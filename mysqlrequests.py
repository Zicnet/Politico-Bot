import disnake
import mysql.connector
from message import messages
from config import mysqlconfig

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
            self.check = False
            return
        
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

    async def reply(self,ctx, redgreen, head, text):
        if text in messages:
            text = messages[text]
        if redgreen:
            color = disnake.Colour.from_rgb(51, 153, 102)
        else:
            color = disnake.Colour.from_rgb(255, 102, 102)
        embed = disnake.Embed(
            title=head,
            description=text,
            colour=color
        )
        await ctx.response.send_message(embed=embed)

        return
