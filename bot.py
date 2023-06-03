import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

import discord_reply
from config import settings, main_guild_scr
import bot_logic
import mysqlrequests


intents = disnake.Intents.default()

main_guild_object = None
intents.voice_states = True
intents.message_content = True 

bot = commands.Bot(
    command_prefix=settings['prefix'],
    intents=disnake.Intents.all(),
    activity=disnake.Game('Zicnet'),
    status=disnake.Status.streaming
)


@bot.event
async def on_ready():
    global main_guild_object
    discord_reply.guild_object = bot.get_guild(1112211843914670100)
    main_guild_object = bot.get_guild(1112211843914670100)
    print(f"{datetime.now()} Bot ready")


@bot.event
async def on_message(message):
    msg = message.content.lower()
    try:
        message.guild.id == None 
    except AttributeError:
        if msg == "start":
            guild = bot.get_guild(settings['guild'])
            await bot_logic.register(message,guild)


@bot.slash_command(name='activity', description='Activity')
async def activity(ctx):
    await ctx.response.defer()
    player =  mysqlrequests.User(ctx.author.id)
    player = player.player
    await ctx.send(
        "Чем хотите заняться?", 
        components = [
            disnake.ui.Button(label="🛹 | Гулять", style=disnake.ButtonStyle.gray, custom_id="status_walk"),
            disnake.ui.Button(label="🚗 | Работать", style=disnake.ButtonStyle.gray, custom_id="status_job"),
            disnake.ui.Button(label="🦽 | Учеба", style=disnake.ButtonStyle.gray, custom_id="status_study"),
            disnake.ui.Button(label="🌃 | Ночной клуб", style=disnake.ButtonStyle.gray, custom_id="status_nightclub"),
            disnake.ui.Button(label="🚤 | Постоять у яхты", style=disnake.ButtonStyle.gray, custom_id="status_stand_by_the_boat")
        ]
    )


@bot.slash_command(name='info', description='Registration')
async def info(ctx):
    await bot_logic.info(ctx)


@bot.slash_command(guild_ids=main_guild_scr, name='echo', description='echo')
@commands.has_permissions(administrator=True)
async def echo(ctx, text: str):
    channel = ctx.channel
    print(channel)
    await channel.send(text)
    await ctx.author.send(f'Я отправил сообщение: {text} | в канал {channel}')


@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id not in [
            "status_walk", 
            "status_job",
            "status_study",
            "status_nightclub",
            "status_stand_by_the_boat"
        ]:
        return
    player =  mysqlrequests.User(inter.author.id)
    player = player.player
    if player.status != 'free':
        return
    if inter.component.custom_id == "status_walk":
        await inter.response.send_message("Вы ушли в лес, на прогулку")
        await bot_logic.joborwalk(player, 'walk')
    elif inter.component.custom_id == "status_job":
        await inter.response.send_message("Вы ушли плакать на работу")
        await bot_logic.joborwalk(player, 'job')
    elif inter.component.custom_id == "status_study":
        await inter.response.send_message("Вы ушли тратить свою жизнь на учебу")
        await bot_logic.joborwalk(player, 'status_study')
    elif inter.component.custom_id == "status_nightclub":
        await inter.response.send_message("Вы все же одумались и пошли в ночной клуб")
        await bot_logic.joborwalk(player, 'status_nightclub')
    elif inter.component.custom_id == "status_stand_by_the_boat":
        await inter.response.send_message("Зачеть имеет яхту, если возле нее можно просто постоять?")
        await bot_logic.joborwalk(player, 'status_stand_by_the_boat')
    


@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send("У вас недостаточно прав команды ``/echo``.")


print(f"{datetime.now()} Bot start")
bot.run(settings['token'])