import re
import asyncio
from datetime import datetime
from functools import partial

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from arq import ArqRedis

from bot.db.db_func import *
from bot.keyboards.user_keyboards import get_main_kb
from bot.logging.logger import logger
from bot.other_func.reminder_analysis import analyze_reminder_handlers

async def cmd_start(message: types.Message) -> None:
    """Обработать команду /start и отправить приветственное сообщение.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    logger.log('info', f'Команда /start выполнена пользователем: {message.from_user.id}')

    await get_user(message=message)

    start_text = (
        "Привет! Я NudgeNinja, Ваш личный бот-напоминалка. "
        "Я здесь, чтобы помочь Вам оставаться организованным и не пропустить ни одного важного события.\n\n"
        "Просто напишите мне, что и когда вам нужно вспомнить, и я установлю напоминание для вас ⏰.\n\n"
        "Например, вы можете сказать: “Напомни мне о встрече завтра в 15:00”, и я установлю напоминание на "
        "указанное время и дату 🥷.\n\n"
        "⚠ <b>Если вы не указали дату, я отправлю Вам напоминание сегодня.</b>"
    )

    await message.answer(start_text, parse_mode="html", reply_markup=get_main_kb())
    logger.log('info', f'Приветственное сообщение отправлено пользователю: {message.from_user.id}')


async def list_reminder(message: types.Message) -> None:
    """Отправить пользователю список напоминаний.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    logger.log('info', f'Запрос списка напоминаний от пользователя: {message.from_user.id}')

    try:
        list_message = "🥷 Вот список ваших напоминаний 📃\n"
        reminders = await get_all_reminders(message)

        # Проверка на наличие напоминаний
        if not reminders:
            logger.log('info', f'Список напоминаний пуст для пользователя: {message.from_user.id}')
            raise TypeError("Список напоминаний пуст")

        for i, reminder in enumerate(reminders, 1):
            list_message += f'\n{i}. Напоминание: "{reminder["text"]}", Дата и время: {reminder["datetime"]}'
            logger.log('info', f'Напоминание {i}: "{reminder["text"]}", Дата и время: {reminder["datetime"]} для пользователя: {message.from_user.id}')

        await message.answer(list_message)

    except TypeError:
        await message.answer("Список напоминаний пуст")
        logger.log('error', f'Ошибка: Список напоминаний пуст для пользователя: {message.from_user.id}')
    except Exception as e:
        await message.answer("Произошла ошибка")
        logger.log('error', f'Произошла ошибка: {e}')


async def get_reminder_text(message: types.Message, redis_pool: ArqRedis) -> None:
    """Анализировать и установить напоминание на основе ввода пользователя.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
        redis_pool (ArqRedis): Пул соединений Redis для планирования задач.
    """
    logger.log('info', f'Получение текста напоминания от пользователя: {message.from_user.id}')

    try:
        await message.answer("Идёт анализ вашего напоминания...")
        logger.log('info', f'Отправка сообщения об анализе напоминания для пользователя: {message.from_user.id}')

        text_remind, from_date, date_str, time_str = await analyze_reminder_handlers(message=message)

        # Проверка на корректность времени для установки напоминания
        if from_date < datetime.now():
            ex_message = "⚠ Минимальное время - 1 минута"
            await message.answer(ex_message)
            logger.log('error', f'Попытка установить напоминание через минуту для пользователя: {message.from_user.id}')
        else:
            await message.answer(f'📝 Ваше напоминание: "{text_remind}"\n🗓 Дата: {date_str} \n⏰ Время: {time_str}')
            await redis_pool.enqueue_job("send_message", _defer_until=from_date, chat_id=message.from_user.id, 
                                           text=f"Пришло время:\n{text_remind}")
            await set_info_remind(message=message)
            logger.log('info', f'Напоминание установлено для пользователя: {message.from_user.id}, текст: "{text_remind}", время: {from_date}')
            asyncio.create_task(delete_expired_rows())

    except (IndexError, ValueError) as e:
        await message.reply("⚠ Введите напоминание еще раз, но, указав дату и время 🥷\n⚠ Минимальное время - 1 минута 🥷")
        logger.log('error', f'Ошибка при анализе напоминания для пользователя: {message.from_user.id}. Ошибка: {e}')
    except Exception as e:
        await message.reply("Произошла ошибка при анализе напоминания.")
        logger.log('error', f'Произошла ошибка для пользователя: {message.from_user.id}. Ошибка: {e}')


async def handle_delete_reminder(message: types.Message) -> None:
    """Обработать удаление напоминания.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    logger.log('info', f'Команда /delete_reminder выполнена пользователем: {message.from_user.id}')

    try:
        # Проверка на корректный номер напоминания
        reminder_number = int(message.text.split()[1])
        reminders = await get_all_reminders(message)

        if reminder_number < 1 or reminder_number > len(reminders):
            raise ValueError("Номер напоминания вне диапазона.")

        reminder_id = reminders[reminder_number - 1]['id']
        result = await delete_reminder(message, reminder_id)
        await message.reply(result)
        logger.log('info', f'Напоминание с ID {reminder_id} удалено для пользователя: {message.from_user.id}')
    except (IndexError, ValueError) as e:
        await message.reply("Пожалуйста, укажите корректный номер напоминания.")
        logger.log('error', f'Ошибка: неверный номер напоминания для пользователя: {message.from_user.id}. Ошибка: {e}')
    except Exception as e:
        await message.reply("Произошла ошибка при удалении напоминания.")
        logger.log('error', f'Произошла ошибка для пользователя: {message.from_user.id}. Ошибка: {e}')


async def handle_edit_reminder(message: types.Message) -> None:
    """Обработать редактирование напоминания.

    Аргументы:
        message (types.Message): Входящее сообщение от пользователя.
    """
    logger.log('info', f'Команда /edit_reminder выполнена пользователем: {message.from_user.id}')

    try:
        # Проверка на корректность формата ввода
        match = re.match(r'/edit_reminder (\d+) (.+) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', message.text)
        if not match:
            raise ValueError("Недостаточно аргументов.")

        reminder_number = int(match.group(1))
        new_text = match.group(2)
        new_date_str = match.group(3)

        new_date = datetime.strptime(new_date_str, "%Y-%m-%d %H:%M:%S")

        reminders = await get_all_reminders(message)

        # Проверка на корректный номер напоминания
        if reminder_number < 1 or reminder_number > len(reminders):
            raise ValueError("Номер напоминания вне диапазона.")

        reminder_id = reminders[reminder_number - 1]['id']
        result = await update_reminder(reminder_id, new_text, new_date, message.from_user.id)
        await message.reply(result)
        logger.log('info', f'Напоминание с ID {reminder_id} обновлено для пользователя: {message.from_user.id}')

    except ValueError as e:
        await message.reply("Пожалуйста, укажите корректный номер напоминания, новый текст и дату.")
        logger.log('error', f'Ошибка: {e} для пользователя: {message.from_user.id}')

    except Exception as e:
        await message.reply("Произошла ошибка при редактировании напоминания.")
        logger.log('error', f'Произошла ошибка для пользователя: {message.from_user.id}. Ошибка: {e}')


def register_user_handlers(dp: Dispatcher, redis_pool: ArqRedis) -> None:
    """Зарегистрировать обработчики команд пользователя в диспетчере.

    Аргументы:
        dp (Dispatcher): Диспетчер для регистрации обработчиков.
        redis_pool (ArqRedis): Пул соединений Redis для планирования задач.
    """
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(handle_delete_reminder, commands=['delete_reminder'])
    dp.register_message_handler(handle_edit_reminder, commands=['edit_reminder'])
    dp.register_message_handler(list_reminder, Text(equals="Список моих напоминаний"))
    dp.register_message_handler(partial(get_reminder_text, redis_pool=redis_pool))  # type: ignore