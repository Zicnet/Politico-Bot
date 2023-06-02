import mysqlrequests


def gl_add_exp(user, count):
    user.player.add_exp(count) # добавление опыта в дб
    level_check = mysqlrequests.Exp.get_current_level(user.player.exp) # возможный лвл с его exp
    if level_check > user.player.level: # сравнение возможного с текущим
        x = level_check - user.player.level # возможный -  текущий (лвл)
        y = 0
        while y < x:
            y += 1
            # отсюда отправить сообщение в лс
            user.player.add_level()
        return True
    return False

user = mysqlrequests.User(619181347084304386)
CurrentLevel = user.player.level
GetNeedXp =  mysqlrequests.Exp.get_need_xp(CurrentLevel+1)
user.player.add_exp(5)
print(GetNeedXp - user.player.exp)