import os

from aiogram import Bot
from arq.connections import RedisSettings
from dotenv import load_dotenv

load_dotenv('.env')

async def startup(ctx: dict) -> None:
    """Инициализировать бота при запуске.

    Аргументы:
        ctx (dict): Контекст, в который будет добавлен объект бота.
    """
    ctx['bot'] = Bot(token=os.getenv("TOKEN_API"))

async def shutdown(ctx: dict) -> None:
    """Закрыть сессию бота при завершении работы.

    Аргументы:
        ctx (dict): Контекст, содержащий объект бота.
    """
    await ctx['bot'].session.close()

async def send_message(ctx: dict, chat_id: int, text: str) -> None:
    """Отправить сообщение в указанный чат.

    Аргументы:
        ctx (dict): Контекст, содержащий объект бота.
        chat_id (int): ID чата, куда будет отправлено сообщение.
        text (str): Текст сообщения для отправки.
    """
    bot: Bot = ctx['bot']
    await bot.send_message(chat_id, text)

class WorkerSettings:
    """Настройки рабочего процесса для ARQ.

    Атрибуты:
        redis_settings (RedisSettings): Настройки подключения к Redis.
        on_startup (callable): Функция для выполнения при запуске.
        on_shutdown (callable): Функция для выполнения при завершении работы.
        functions (list): Список функций, доступных для выполнения.
    """
    redis_settings = RedisSettings
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message]