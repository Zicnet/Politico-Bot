import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

from config import settings
import bot_logic

# config
intents = disnake.Intents.default()
main_guild = 1112211843914670100
main_guild_scr = [1112211843914670100]
intents.voice_states = True
intents.message_content = True  # Добавьте эту строку

# Bot config and sql connector
bot = commands.Bot(
    command_prefix=settings['prefix'],
    intents=disnake.Intents.all(),
    activity=disnake.Game('Zicnet'),
    status=disnake.Status.streaming
)


# bot event
@bot.event
async def on_ready():
    print(f"{datetime.now()} Bot ready")

@bot.event
async def on_message(message):
    msg = message.content.lower()
    try:
        message.guild.id == None 
    except AttributeError:
        if msg == "start":
            guild = bot.get_guild(main_guild)
            await bot_logic.register(message,guild)


@bot.slash_command(name='info', description='Registration')
async def info(ctx):
    await bot_logic.info(ctx)


# bot command
@bot.slash_command(guild_ids=test_guilds,
                   name='register',
                   description='Registration')
async def register(ctx, role: disnake.Role):
    bot_logic.register(ctx, role)


@bot.slash_command(guild_ids=test_guilds,
                   name='info',
                   description='Registration')
async def info(ctx, member: disnake.Member):
    bot_logic.info(ctx, member)

print(f"{datetime.now()} Bot start")
bot.run(settings['token'])