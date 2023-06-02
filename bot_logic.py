import datetime
from datetime import datetime
from datetime import timedelta
import math
import asyncio

from disnake.utils import get
from apscheduler.schedulers.asyncio import AsyncIOScheduler


import game_logic
import mysqlrequests
import discord_reply

async def register(ctx, guild):
    discordUser = ctx.author
    discordUser = guild.get_member(discordUser.id)
    party = mysqlrequests.PoliticalOpinion(0)
    discordRole = get(guild.roles, name=party.name)
    user = mysqlrequests.User(discordUser.id)
    discordMainRole = get(guild.roles, name="*")
    await discordUser.add_roles(discordMainRole)
    if user.check:
        await discord_reply.send_to(discordUser, False, 'Регистрация', 'isAlreadyRegistered')
        party = user.player.political_opinion
        discordRole = get(guild.roles, name=party.name)
        await discordUser.add_roles(discordRole)
        return
    user.db_register()
    await discordUser.add_roles(discordRole)
    await discord_reply.send_to(discordUser, True, 'Успешная регистрация', 'kykold')


async def info(ctx):
    user = ctx.author
    client = mysqlrequests.User(user.id)
    if not client.check:
        await discord_reply.reply(ctx, False, 'Регистрация', 'regerror')
        return
    await discord_reply.reply_info(ctx, 'Info')


async def joborwalk(player, job_type):
    scheduler = AsyncIOScheduler()
    user = mysqlrequests.User(player.id)
    walk_and_job_list = await game_logic.job_exp_list(player.level, job_type)
    player.set_status(job_type)
    async def cooldown():
        await discord_reply.send_to_id(user.discord_id, True, "Работа", "Завершил действие")
        player.add_money(walk_and_job_list['money'])
        await game_logic.gl_add_exp(user, walk_and_job_list['exp'])
        player.set_status("free")
        scheduler.shutdown
    date_now = datetime.now()
    min= date_now + timedelta(seconds=60*5)
    scheduler.add_job(cooldown, trigger="cron", minute=min.minute)
    scheduler.start()

