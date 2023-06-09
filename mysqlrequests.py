import mysql.connector

import discord_reply
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
    def __init__(self, value_request):
        self.value_request = value_request
        self.discord_id = None
        self.id = None
        self.date_registrator = None
        self.player = None
        if not self.user_check():
            return
        self.check = True
        self.user_update()

    def user_check(self):
        cur = con.cursor()

        # Получаем информацию о пользователе из базы данных по его discord_id
        cur.execute(
            f"SELECT id FROM user WHERE discord_id = {self.value_request} OR id = {self.value_request}")
        record = cur.fetchone()
        self.check = False if record is None else True
        return self.check

    def user_update(self):
        cur = con.cursor()

        # Получаем информацию о пользователе из базы данных по его discord_id
        cur.execute(
            f"SELECT id, discord_id, date_registrator FROM user WHERE discord_id = {self.value_request} OR id = {self.value_request}")
        record = cur.fetchone()

        self.id = record[0]
        self.discord_id = record[1]
        self.date_registrator = record[2]
        self.player = Player(self.id)

    def db_register(self):
        if self.check:
            return
        cur = con.cursor()
        if self.check:
            return
        # Регистрируем пользователя в базе данных
        cur.execute(
            f"INSERT INTO user(discord_id, date_registrator) VALUES({self.discord_id},  '{datetime.now().date()}')")
        con.commit()
        cur.close()
        self.user_update()
        self.player.create_new_player()
        self.user_update()


class Player:
    def __init__(self, request_id):
        self.request_id = request_id
        self.id = None
        self.political_opinion_id = None
        self.political_opinion = None
        self.money = None
        self.status = None
        self.exp = None
        self.level = None
        self.check = self.user_check()
        self.player_update()

    def user_check(self):
        cur = con.cursor()
        cur.execute(
            f"SELECT id FROM player WHERE id = {self.request_id}")
        record = cur.fetchone()
        self.check = False if record is None else True
        return self.check

    def create_new_player(self):
        if self.check:
            return
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO player(id, status) VALUES({self.request_id}, 'free')")
        con.commit()
        cur.close()
        self.player_update()

    def player_update(self):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(
            f"SELECT id, political_opinion_id, money, status, exp, level FROM player WHERE id = {self.request_id}")
        record = cur.fetchone()
        self.id = record[0]
        self.political_opinion_id = record[1]
        self.money = record[2]
        self.status = record[3]
        self.exp = record[4]
        self.level = record[5]
        self.political_opinion = PoliticalOpinion(self.political_opinion_id)

    def set_money(self, money):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET money = '{money}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()

    def add_money(self, money):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET money = '{self.money + money}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()

    def set_political_opinion(self, request_opinion_id):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET political_opinion_id = '{request_opinion_id}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()

    def add_exp(self, point):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET exp = '{self.exp+point}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()

    def add_level(self):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET level = '{self.level+1}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()

    def set_status(self, status):
        if not self.check:
            return
        cur = con.cursor()
        cur.execute(f"UPDATE player SET status = '{status}' WHERE id = {self.id}")
        con.commit()
        cur.close()
        self.player_update()


class PoliticalOpinion:
    def __init__(self, request):
        self.request = request
        self.id = None
        self.name = None
        self.discord_id = None
        self.color = None
        self.check = None
        if not self.opinion_check():
            return
        self.get_opinion()

    def opinion_check(self):
        cur = con.cursor()
        cur.execute(
            f"SELECT id FROM opinion WHERE id = {self.request} OR name = '{self.request}' OR discord_id = '{self.request}';"
        )
        record = cur.fetchone()
        self.check = False if record is None else True
        return self.check

    def get_opinion(self):
        cur = con.cursor()
        cur.execute(
            f"SELECT id, name, discord_id, color FROM opinion WHERE id = {self.request} OR name = '{self.request}' OR discord_id = '{self.request}';"
        )
        record = cur.fetchone()
        self.id = record[0]
        self.name = record[1]
        self.discord_id = record[2]
        self.color = record[3]


class Exp:
    def get_need_xp(level):
        cur = con.cursor()
        cur.execute(
            f"SELECT exp_exp FROM exp WHERE exp_lvl = {level}"
        )
        record = cur.fetchone()
        req = 999999999 if record is None else record[0]
        return req

    def get_current_level(exp):
        cur = con.cursor()
        cur.execute(
            f"SELECT MAX(exp_lvl) exp_lvl FROM exp WHERE exp_exp <= {exp}"
        )
        record = cur.fetchone()
        return record[0]