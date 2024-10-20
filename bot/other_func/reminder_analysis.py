from datetime import datetime
import periodparser as pp
from aiogram import types

async def analyze_reminder_handlers(message: types.Message) -> tuple[str, datetime, str, str]:
    """Анализировать текст сообщения и извлечь напоминание и дату.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.

    Возвращает:
        tuple: Кортеж, содержащий текст напоминания, дату начала,
               строковое представление даты и время.
    """
    user_message = message.text

    result_text = pp.extract(user_message)
    result_text.tokens.remove('{0}')
    text_remind = ' '.join(result_text.tokens)
    from_date = result_text.dates[0].date_from

    date_str = from_date.strftime("%d %B")
    time_str = from_date.strftime("%H:%M")

    return text_remind, from_date, date_str, time_str


async def analyze_reminder_db(message: types.Message) -> tuple[str, datetime]:
    """Анализировать текст сообщения и извлечь напоминание и дату для базы данных.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.

    Возвращает:
        tuple: Кортеж, содержащий текст напоминания и дату начала.
    """
    user_message = message.text

    result_text = pp.extract(user_message)
    result_text.tokens.remove('{0}')
    text_remind = ' '.join(result_text.tokens)
    from_date = result_text.dates[0].date_from

    return text_remind, from_date