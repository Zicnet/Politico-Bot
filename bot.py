import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

from config import settings
import bot_logic

# config
intents = disnake.Intents.default()
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
@bot.slash_command(name='register', description='Registration')
async def register(ctx, role: disnake.Role):
    await bot_logic.register(ctx, role)


@bot.slash_command(name='info', description='Registration')
async def info(ctx):
    await bot_logic.info(ctx)

print(f"{datetime.now()} Bot start")
bot.run(settings['token'])