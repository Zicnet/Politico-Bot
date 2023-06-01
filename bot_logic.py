import datetime
from datetime import datetime

from disnake.utils import get

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