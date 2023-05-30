import mysql.connector
from config import mysqlconfig
from datetime import datetime

# Устанавливаем соединение с базой данных MySQL
con = mysql.connector.connect(
    host=mysqlconfig["host"],  # Адрес хоста базы данных
    user=mysqlconfig["user"],  # Имя пользователя базы данных
    password=mysqlconfig["password"],  # Пароль пользователя базы данных
    database=mysqlconfig["db_name"],  # Имя базы данных
)
cur = con.cursor()


class User:
    def __init__(self, discordID):
        self.discord_id = discordID
        self.id = None
        self.balance = None
        self.political_opinion = None
        self.date_registrator = None
        if not self.user_check():
            return
        self.user_update()

    def user_check(self):
        cur = con.cursor()

        # Получаем информацию о пользователе из базы данных по его discord_id
        cur.execute(
            f"SELECT id FROM user WHERE discord_id = {self.discord_id}")
        record = cur.fetchone()
        self.check = False if record is None else True
        return self.check

    def user_update(self):
        cur = con.cursor()

        # Получаем информацию о пользователе из базы данных по его discord_id
        cur.execute(
            f"SELECT id, discord_id, balance, political_opinion, date_registrator FROM user WHERE discord_id = {self.discord_id}")
        record = cur.fetchone()

        self.id = record[0]
        self.discord_id = record[1]
        self.balance = record[2]
        self.political_opinion = record[3]
        self.date_registrator = record[4]

    def balance(self, money):
        cur = con.cursor()

        # Обновляем баланс пользователя в базе данных
        cur.execute(f"UPDATE user SET balance = '{money}' WHERE discord_id = {self.discord_id}")
        con.commit()
        cur.close()
        self.user_update()

    def political_opinion(self, string):
        cur = con.cursor()

        # Обновляем политическое мнение пользователя в базе данных
        cur.execute(f"UPDATE user SET political_opinion = '{string}' WHERE discord_id = {self.discord_id}")
        con.commit()
        cur.close()
        self.user_update()

    def db_register(self, role_id):
        cur = con.cursor()

        # Регистрируем пользователя в базе данных
        cur.execute(
            f"INSERT INTO user(discord_id,balance,political_opinion,date_registrator) VALUES({self.discord_id}, '0', '{role_id}', '{datetime.now().date()}')")
        con.commit()
        cur.close()
        self.user_update()

