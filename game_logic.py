import math

import mysqlrequests
import discord_reply
import walk_and_job_exp


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


async def job_exp_list(player_level, job_type):
    scale_player_level = math.floor(player_level / 5) * 5
    get_type_list = walk_and_job_exp.exp_list[job_type]
    get_type_list = get_type_list[scale_player_level]
    return get_type_list
