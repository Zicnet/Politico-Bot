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
import discord_reply

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


# bot event
@bot.event
async def on_ready():
    print(f"{datetime.now()} Bot ready")


# bot command
@bot.slash_command(guild_ids=test_guilds,
                    name='register',
                    description='Registration')
async def register(ctx, opponent: disnake.Member, political_opinion = disnake.Role):
    member = ctx.author # получаем чела
    role = disnake.utils.get(ctx.guild.roles, id=political_opinion)     # получаем объект роли, для вписанной роли
    client = mysqlrequests.User(member.id)
    if client.check:
        await discord_reply.reply(ctx, False, 'Регистрация', 'regerror')
        return
    client.db_register(political_opinion)   # регаем в базе
    await opponent.add_roles(role)  # какидываем роль
    await discord_reply.reply(ctx, False, 'Регистрация', 'regerror')

@bot.slash_command(guild_ids=test_guilds,
                    name='register',
                    description='Registration')
async def register(ctx, member: disnake.Member):
    member = ctx.author
    client = mysqlrequests.User(member.id)
    if client.check:
        await discord_reply.reply(ctx, False, 'Регистрация', 'regesuc')
        return
    await discord_reply.reply_info(ctx, 'Info')
    
    
    



print(f"{datetime.now()} Bot start")
bot.run(settings['token'])
