import mysql.connector
from config import mysqlconfig
from datetime import datetime

con = mysql.connector.connect(
    host=mysqlconfig["host"],
    user=mysqlconfig["user"],
    password=mysqlconfig["password"],
    database=mysqlconfig["db_name"],
)
cur = con.cursor()


class User:
    def __init__(self, discordID):
        cur = con.cursor()
        cur.execute(f"SELECT id, discord_id, balance, political_opinion, date_registrator FROM user WHERE discord_id = {discordID}")
        record = cur.fetchone()

        if record is None:
            self.discord_id = discordID
            self.check = False
        else:
            self.check = True
            self.id = record[0]
            self.discord_id = record[1]
            self.balance = record[2]
            self.political_opinion = record[3]
            self.date_registrator = record[4]

    def balance(self, money):
        cur = con.cursor()
        cur.execute(f"UPDATE user SET balance = '{money}' WHERE discord_id = {self.discord_id}")
        con.commit()
        cur.close()

    def political_opinion(self, string):
        cur = con.cursor()
        cur.execute(f"UPDATE user SET political_opinion = '{string}' WHERE discord_id = {self.discord_id}")
        con.commit()
        cur.close()

    def db_register(self, role_id):
        cur = con.cursor()
        print(self)

        cur.execute(
            f"INSERT INTO user(discord_id,balance,political_opinion,date_registrator) VALUES({self.discord_id}, '0', '{role_id}', '{datetime.now().date()}')")
        con.commit()
        cur.close()
