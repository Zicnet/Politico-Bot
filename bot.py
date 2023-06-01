import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

from config import settings
import bot_logic

# config
intents = disnake.Intents.default()
test_guilds = [1112211843914670100]
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
@bot.slash_command(guild_ids=test_guilds, name='register',description='Registration')
async def register(ctx, role: disnake.Role):
    await bot_logic.register(ctx, role)


@bot.slash_command(guild_ids=test_guilds, name='info',description='Registration')
async def info(ctx, member: disnake.Member):
    await bot_logic.info(ctx, member)

print(f"{datetime.now()} Bot start")
bot.run(settings['token'])