import disnake
import datetime
import mysqlrequests
import mysql.connector
from message import messages
from mysqlrequests import User
from datetime import datetime
from disnake.ext import commands
from config import settings
from config import mysqlconfig


# config
balance = mysqlrequests.User.balance
political_opinion = mysqlrequests.User.political_opinion
intents = disnake.Intents.default()
test_guilds=[1112211843914670100]
intents.voice_states = True


# Bot config and sql connector
bot = commands.Bot(
    command_prefix=settings['prefix'],
    help_command=None,
    intents=disnake.Intents.all(),
    activity=disnake.Game('Zicnet'),
    status=disnake.Status.streaming
)
con = mysql.connector.connect(
    host=mysqlconfig["host"],
    user=mysqlconfig["user"],
    password=mysqlconfig["password"],
    database=mysqlconfig["db_name"],
)
cur = con.cursor()


# bot event
@bot.event
async def on_ready():
    print(f"{datetime.now()} Bot ready")


# bot command
@bot.slash_command(guild_ids=test_guilds,
                    name='register',
                    description='Registration')
async def register(ctx, opponent: disnake.Member, political_opinion = disnake.Role):
    member = ctx.author
    role = disnake.utils.get(ctx.guild.roles, id=political_opinion)
    await opponent.add_roles(role)
    reply = mysqlrequests.User.reply
    client = mysqlrequests.User(member.id)
    if client.check == True:
        await client.reply(ctx, False, 'Регистрация', 'regerror')
        return

    cur = con.cursor()
    cur.execute(f"INSERT INTO user(discord_id,balance,political_opinion,date_registrator) VALUES({opponent.id}, '0', '{political_opinion}','{datetime.now().date()}')")
    con.commit()
    cur.close()

print(f"{datetime.now()} Bot start")
bot.run(settings['token'])
