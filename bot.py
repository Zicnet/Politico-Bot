import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

from config import settings
import bot_logic

# config
intents = disnake.Intents.default()
main_guild = [1112211843914670100]
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


# bot command
@bot.slash_command(name='register', description='Registration')
async def register(ctx, role: disnake.Role):
    await bot_logic.register(ctx, role)


@bot.slash_command(name='info', description='Registration')
async def info(ctx):
    await bot_logic.info(ctx)


@bot.slash_command(guild_ids=main_guild, name='echo', description='echo')
@commands.has_permissions(administrator=True)
async def echo(ctx, text: str):
    channel = ctx.channel
    print(channel)
    await channel.send(text)
    await ctx.author.send(f'Я отправил сообщение: {text} | в канал {channel}')


@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send("У вас недостаточно прав команды ``/echo``.")

print(f"{datetime.now()} Bot start")
bot.run(settings['token'])