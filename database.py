import mysql.connector
from config import Config

class DB:
    def __init__(self):
        # устанавливаем соединение с базой данных
        self.conn = mysql.connector.connect(
            user=Config.DB.user,
            password=Config.DB.password,
            host=Config.DB.host,
            port=Config.DB.port,
            database=Config.DB.database
        )

        # создаем таблицу расписания, если ее еще нет
        self.create_table()

    def create_table(self):
        # создаем таблицу расписания
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                time VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL
            )
        """)
        self.conn.commit()

    def add_schedule(self, name, time, description):
        # добавляем новую запись в расписание
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO schedule (name, time, description)
            VALUES (%s, %s, %s)
        """, (name, time, description))
        self.conn.commit()

    def delete_schedule(self, name):
        # удаляем запись из расписания
        cur = self.conn.cursor()
        cur.execute("""
            DELETE FROM schedule WHERE name = %s
        """, (name,))
        self.conn.commit()

    def show_schedule(self):
        # получаем все записи из расписания
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM schedule")
        return cur.fetchall()
