import datetime
from datetime import datetime

import mysqlrequests
import discord_reply


async def register(ctx, role):
    member = ctx.author  # получаем чела
    client = mysqlrequests.User(member.id)
    pol_opinion = mysqlrequests.PoliticalOpinion(role.id)
    if client.check:
        await discord_reply.reply(ctx, False, 'Регистрация', 'regerror')
        return
    await discord_reply.reply(ctx, True, 'Регистрация', 'regesuc')
    client.db_register()  # регаем в базе
    client.player.set_political_opinion(pol_opinion.id)
    await member.add_roles(role)  # какидываем роль


async def info(ctx, user):
    client = mysqlrequests.User(user.id)
    if not client.check:
        await discord_reply.reply(ctx, False, 'Регистрация', 'regerror')
        return
    await discord_reply.reply_info(ctx, 'Info')