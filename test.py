import datetime
import pytz
import time

def countdown_to_june_1():
    target_date = datetime.datetime(datetime.datetime.now().year, 6, 1)

    if datetime.datetime.now().month > 6 or (datetime.datetime.now().month == 6 and datetime.datetime.now().day > 1):
        target_date = datetime.datetime(datetime.datetime.now().year + 1, 6, 1)

    target_date = pytz.timezone('Europe/Kiev').localize(target_date)
    current_timezone = pytz.timezone('Europe/Kiev')

    while True:
        current_time = datetime.datetime.now(current_timezone)
        time_remaining = target_date - current_time

        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"Осталось до 1 июня: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд.")
        if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            break

        time.sleep(1)

countdown_to_june_1()
