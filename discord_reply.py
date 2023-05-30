import disnake
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