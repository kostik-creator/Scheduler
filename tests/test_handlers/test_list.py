import pytest
from unittest.mock import AsyncMock, patch

from bot.handlers.user_handlers import list_reminder

@pytest.mark.asyncio
async def test_list_reminder() -> None:
    """Тест для получения списка напоминаний.

    Проверяет, что функция корректно возвращает список напоминаний пользователю
    и логирует соответствующие сообщения.
    """
    message = AsyncMock()
    message.from_user.id = 12345

    reminders = [
        {'text': 'Напоминание 1', 'datetime': '2024-10-19 15:00:00'},
        {'text': 'Напоминание 2', 'datetime': '2024-10-20 16:00:00'}
    ]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders:

        mock_get_all_reminders.return_value = reminders

        await list_reminder(message)

        expected_message = """🥷 Вот список ваших напоминаний 📃\n
1. Напоминание: "Напоминание 1", Дата и время: 2024-10-19 15:00:00
2. Напоминание: "Напоминание 2", Дата и время: 2024-10-20 16:00:00"""

        message.answer.assert_called_with(expected_message)
        mock_log.assert_any_call('info', f'Запрос списка напоминаний от пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Напоминание 1: "Напоминание 1", Дата и время: 2024-10-19 15:00:00 для пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Напоминание 2: "Напоминание 2", Дата и время: 2024-10-20 16:00:00 для пользователя: {message.from_user.id}')


@pytest.mark.asyncio
async def test_list_reminder_empty() -> None:
    """Тест для обработки случая, когда список напоминаний пуст.

    Проверяет, что функция отправляет сообщение о пустом списке
    и логирует соответствующие сообщения об ошибке.
    """
    message = AsyncMock()
    message.from_user.id = 12345

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders:

        mock_get_all_reminders.return_value = []

        await list_reminder(message)

        message.answer.assert_called_with("Список напоминаний пуст")
        mock_log.assert_any_call('info', f'Запрос списка напоминаний от пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Список напоминаний пуст для пользователя: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Ошибка: Список напоминаний пуст для пользователя: {message.from_user.id}')