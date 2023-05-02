import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# ---------
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import dc
from dc import *
from database import DB
from config import Config
from texts import Text

# ---------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger('telegram.bot').setLevel('ERROR')
logger = logging.getLogger(__name__)
logger.info('Folder "parrent" is: ' + parent)
# инициализация базы данных
db = DB()

# функция приветствия
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Text.start_message)

# функция вывода списка команд
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Text.help_message)

# функция для добавления записи в расписание
def add_schedule(update, context):
    try:
        # получаем параметры для новой записи
        args = context.args
        name = args[0]
        time = args[1]
        description = " ".join(args[2:])

        # добавляем новую запись в расписание
        db.add_schedule(name, time, description)
        update.message.reply_text(Text.add_schedule_success)

    except (IndexError, ValueError):
        update.message.reply_text(Text.help_message)


# функция для удаления записи из расписания
def delete_schedule(update, context):
    try:
        # получаем название записи, которую нужно удалить
        name = context.args[0]

        # удаляем запись из расписания
        db.delete_schedule(name)
        update.message.reply_text(Text.delete_schedule_success)

    except (IndexError, KeyError):
        update.message.reply_text(Text.help_message)


# функция для вывода расписания
def show_schedule(update, context):
    data = db.show_schedule()
    if not data:
        update.message.reply_text(Text.delete_schedule_not_found)
    else:
        # формируем текст расписания
        text = ""
        for row in data:
            text += f"{row[1]} - {row[2]}: {row[3]}\n"

        # отправляем текст расписания пользователю
        update.message.reply_text(text)


def main() -> None:
    # инициализация бота
    updater = Updater(Config.TG.bot_token, use_context=True)

    # добавляем обработчики команд
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('add_schedule', add_schedule))
    updater.dispatcher.add_handler(CommandHandler('delete_schedule', delete_schedule))
    updater.dispatcher.add_handler(CommandHandler('show_schedule', show_schedule))

    # запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()