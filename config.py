import logging

class Config:
    logger_lvl = logging.DEBUG

    class TG:
        debug = False
        admins = [
            666147669,  # @lexanon - Лёша
            432998089   # @nicookiee - Никита
        ]
        bot_token = '...'

    class DB:
        host = 'localhost'
        port = 3306
        user = '...'
        password = '...'
        database = '...'

    # class DB:
    #     debug = False
    #     # host = 'db'
    #     if debug:
    #         host = 'localhost'
    #         port = 3306
    #         user = 'root'
    #         password = '///'
    #         database = 'bot'
    #     # else:
    #     #     host = 'https://lexanon.me'
    #     #     port = 0
    #     #     user = ''
    #     #     password = ''
    #     #     #database = ''
