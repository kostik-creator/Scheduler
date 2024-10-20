import asyncio
from datetime import datetime
from typing import List, Dict, Optional

from aiogram import types

from bot.db.db_tables import connection
from bot.other_func.reminder_analysis import analyze_reminder_db
from bot.logging.logger import logger

async def get_user(message: types.Message) -> None:
    """Добавить пользователя в базу данных, если его еще нет.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO main_users (tg_id, tg_username) VALUES (%s, %s)""",
                (message.from_user.id, message.from_user.username)
            )
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in get_user: {ex}')


async def delete_expired_rows() -> None:
    """Удалять просроченные напоминания из базы данных каждую минуту."""
    while True:
        try:
            with connection.cursor() as cursor:
                now = datetime.now()
                cursor.execute(
                    """SELECT * FROM main_schedule WHERE reminder_datetime < %s""",
                    (now,)
                )
                rows = cursor.fetchall()

                for row in rows:
                    print(f"Deleting row with id {row[0]} and time {row[2]}")
                    cursor.execute(
                        """DELETE FROM main_schedule WHERE id = %s""",
                        (row[0],)
                    )
            await asyncio.sleep(60)
        except Exception as ex:
            logger.log('error', f'PostgresSQL ERROR in delete_expired_rows: {ex}')


async def get_all_remind(message: types.Message) -> List[str]:
    """Получить все напоминания пользователя.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.

    Возвращает:
        list: Список текстов напоминаний.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT reminder_text FROM main_schedule WHERE fk_user_id = %s""",
                (message.from_user.id,)
            )
            reminders = cursor.fetchall()
            reminders = [reminder[0] for reminder in reminders]
            return reminders
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in get_all_remind: {ex}')
        return []


async def delete_reminder(message: types.Message, reminder_id: int) -> str:
    """Удалить напоминание по его ID.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
        reminder_id (int): ID напоминания для удаления.

    Возвращает:
        str: Результат операции удаления.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM main_schedule WHERE id = %s AND fk_user_id = %s""",
                (reminder_id, message.from_user.id)
            )

            if cursor.rowcount > 0:
                connection.commit()
                return "Напоминание успешно удалено."
            else:
                return "Напоминание не найдено или вы не имеете права его удалять."
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in delete_reminder: {ex}')
        return "Произошла ошибка при удалении напоминания."


async def update_reminder(reminder_id: int, new_text: str, new_date: datetime, user_id: int) -> str:
    """Обновить существующее напоминание.

    Аргументы:
        reminder_id (int): ID напоминания для обновления.
        new_text (str): Новый текст напоминания.
        new_date (datetime): Новая дата и время напоминания.
        user_id (int): ID пользователя, которому принадлежит напоминание.

    Возвращает:
        str: Результат операции обновления.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE main_schedule SET reminder_text = %s, reminder_datetime = %s 
                   WHERE id = %s AND fk_user_id = %s""",
                (new_text, new_date, reminder_id, user_id)
            )

            if cursor.rowcount > 0:
                connection.commit()
                return "Напоминание успешно обновлено!"
            else:
                return "Не удалось обновить напоминание. Пожалуйста, проверьте ID."
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in update_reminder: {ex}')
        return "Произошла ошибка при обновлении напоминания."


async def set_info_remind(message: types.Message) -> None:
    """Сохранить новое напоминание в базе данных.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    try:
        text_remind, from_date = await analyze_reminder_db(message=message)
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO main_schedule (reminder_text, reminder_datetime, fk_user_id) 
                   VALUES (%s, %s, %s)""",
                (text_remind, from_date, message.from_user.id)
            )
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in set_info_remind: {ex}')


async def get_all_reminders(message: types.Message) -> List[Dict[str, Optional[str]]]:
    """Получить все напоминания пользователя с их ID, текстом и временем.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.

    Возвращает:
        list: Список словарей с информацией о напоминаниях.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, reminder_text, reminder_datetime 
                   FROM main_schedule 
                   WHERE fk_user_id = %s""",
                (message.from_user.id,)
            )
            reminders = cursor.fetchall()

            reminders_list = [
                {
                    "id": reminder[0],
                    "text": reminder[1],
                    "datetime": reminder[2]
                }
                for reminder in reminders
            ]
            return reminders_list
    except Exception as ex:
        logger.log('error', f'PostgresSQL ERROR in get_all_reminders: {ex}')
        return []