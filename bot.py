import os
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

import requests


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def today_moscow():
    return datetime.now(MOSCOW_TZ).date()


def get_next_date(month, day, today):
    result = date(today.year, month, day)

    if result < today:
        result = date(today.year + 1, month, day)

    return result


def calendar_days_left(today, end_date):
    return (end_date - today).days + 1


def school_days_left(today, end_date):
    current = today
    count = 0

    while current <= end_date:

        is_weekday = current.weekday() < 5

        is_december_25 = (
            current.month == 12
            and current.day == 25
        )

        if is_weekday and not is_december_25:
            count += 1

        current += timedelta(days=1)

    return count


def calculate():

    today = today_moscow()

    december_31 = get_next_date(
        12,
        31,
        today
    )

    january_22 = get_next_date(
        1,
        22,
        today
    )

    days_to_december = calendar_days_left(
        today,
        december_31
    )

    school_days = school_days_left(
        today,
        december_31
    )

    days_to_january = calendar_days_left(
        today,
        january_22
    )

    return (
        days_to_december,
        school_days,
        days_to_january
    )


def make_message():

    (
        days_to_december,
        school_days,
        days_to_january
    ) = calculate()

    return (
        f"до мозгоебли {days_to_december} дней\n"
        f"Учебных дней {school_days}\n"
        f"До чила релакса на жалкие две недели {days_to_january}"
    )


def send_message():

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": make_message()
    }

    response = requests.post(
        url,
        data=data,
        timeout=30
    )

    response.raise_for_status()

    print("Сообщение успешно отправлено!")
    print(make_message())


if __name__ == "__main__":
    send_message()
