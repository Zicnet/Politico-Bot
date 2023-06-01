import mysqlrequests


async def current_level(ctx):
    member = ctx.author
    user = mysqlrequests.User(member.id)
    CurrentLevel = user.player.level