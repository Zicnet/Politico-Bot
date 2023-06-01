import datetime
from datetime import datetime

import disnake
from disnake.ext import commands

import discord_reply
import mysqlrequests 

async def current_level(ctx):
    member = ctx.author
    user = mysqlrequests.User(member.id)
    CurrentLevel = user.player.level