import disnake
import mysql.connector
import mysqlrequests 
from message import messages


# заготовка для ответов
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


async def reply_info(ctx, head):
    member = ctx.author
    user = mysqlrequests.User(member.id)
    embed = disnake.Embed(title=head, color=member.color)
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.player.status, inline=True)
    embed.add_field(name="Political Opinion", value=user.player.political_opinion.name, inline=True)
    embed.add_field(name="Balance", value=user.player.money, inline=True)
    embed.add_field(name="Date Registrator", value=user.date_registrator, inline=True)
    await ctx.response.send_message(embed=embed)