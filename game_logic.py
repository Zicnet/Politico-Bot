import mysqlrequests
import discord_reply

async def gl_add_exp(user, count):
    user.player.add_exp(count) # добавление опыта в дб
    level_check = mysqlrequests.Exp.get_current_level(user.player.exp) # возможный лвл с его exp
    if level_check > user.player.level: # сравнение возможного с текущим
        x = level_check - user.player.level # возможный -  текущий (лвл)
        y = 0
        while y < x:
            y += 1
            await discord_reply.send_to_id(user.discord_id, True, 'LVLUP', 'LevelHuy')
            user.player.add_level()
        return True
    return False


