import disnake
from disnake.ext import commands
import mysqlrequests 
from message import messages

guild_object = None


# заготовка для ответовs
async def reply(ctx, redgreen, head, text):
    if text in messages:
        text = messages[text]
    if redgreen:
        color = disnake.Colour.from_rgb(51, 153, 102)
    else:
        color = disnake.Colour.from_rgb(255, 102, 102)
    embed = disnake.Embed(
        title=head,
        description=text,
        colour=color
    )
    await ctx.response.send_message(embed=embed)


async def send_to(user, redgreen, head, text):
    if text in messages:
        text = messages[text]
    if redgreen:
        color = disnake.Colour.from_rgb(51, 153, 102)
    else:
        color = disnake.Colour.from_rgb(255, 102, 102)
    embed = disnake.Embed(
        title=head,
        description=text,
        colour=color
    )    
    await user.send(embed=embed)


async def send_to_id(user_id, redgreen, head, text):
    user = guild_object.get_member(user_id)
    if text in messages:
        text = messages[text]
    if redgreen:
        color = disnake.Colour.from_rgb(51, 153, 102)
    else:
        color = disnake.Colour.from_rgb(255, 102, 102)
    embed = disnake.Embed(
        title=head,
        description=text,
        colour=color
    )
    await user.send(embed=embed)


async def reply_info(ctx, head):
    await ctx.response.defer()
    member = ctx.author
    user = mysqlrequests.User(member.id)
    embed = disnake.Embed(title=head, color=member.color)
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.player.status, inline=True)
    embed.add_field(name="Political Opinion", value=user.player.political_opinion.name, inline=True)
    embed.add_field(name="Level", value= user.player.level, inline=True)
    embed.add_field(name="Balance", value=user.player.money, inline=True)
    embed.add_field(name="Date Registrator", value=user.date_registrator, inline=True)
    await ctx.send(embed=embed)