# Запуск проекта
# Для корректной работы приложения выполните следующие шаги:
#
# 1. Убедитесь, что все зависимости установлены:
#    Выполните команду в терминале:
#    ```
#    pip install -r requirements.txt
#    ```
#
# 2. Запустите бота:
#    Откройте терминал и перейдите в директорию с вашим проектом. Затем выполните:
#    ```
#    python main.py
#    ```
#
# 3. Запустите воркер:
#    Откройте второй терминал и выполните:
#    ```
#    arq bot.other_func.arq_func.WorkerSettings
#    ```
#
# Важно:
# - Убедитесь, что файл .env создан и заполнен необходимыми значениями, включая токен вашего Telegram бота (переменная TOKEN_API).
# - Проверьте, что Redis-сервер запущен и доступен по указанным в файле .env параметрам.
#
# Следуя этим шагам, вы сможете успешно запустить ваше приложение и начать взаимодействовать с ботом!

import os
import asyncio

from aiogram import Bot, Dispatcher, types
from arq import create_pool, ArqRedis
from arq.connections import RedisSettings
from dotenv import load_dotenv

from bot.handlers.user_handlers import register_user_handlers

load_dotenv('.env')

def register_handler(dp: Dispatcher, redis_pool: ArqRedis) -> None:
    """Регистрация обработчиков пользователей."""
    register_user_handlers(dp, redis_pool)


async def set_bot_commands(bot: Bot) -> None:
    """Установка команд для бота."""
    commands: list[types.BotCommand] = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/edit_reminder", description="Пример: /edit_reminder 1 Новый текст 2024-10-22 14:30:00"),
        types.BotCommand(command="/delete_reminder", description="Пример: /delete_reminder 1"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    """Основная функция для запуска бота."""
    token: str = os.getenv("TOKEN_API")
    redis_pool: ArqRedis = await create_pool(RedisSettings)

    bot: Bot = Bot(token)
    dp: Dispatcher = Dispatcher(bot)
    register_handler(dp, redis_pool)
    
    await set_bot_commands(bot)
    
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())