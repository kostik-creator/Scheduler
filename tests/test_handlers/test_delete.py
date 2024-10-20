import pytest
from unittest.mock import AsyncMock, patch

from bot.handlers.user_handlers import handle_delete_reminder

@pytest.mark.asyncio
async def test_handle_delete_reminder() -> None:
    """Тест для обработки удаления напоминания.

    Проверяет, что функция корректно удаляет напоминание и отправляет ответ пользователю.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/delete_reminder 1"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders, \
         patch('bot.handlers.user_handlers.delete_reminder', new_callable=AsyncMock) as mock_delete_reminder:
        
        mock_get_all_reminders.return_value = reminders
        mock_delete_reminder.return_value = "Напоминание удалено"
        
        await handle_delete_reminder(message)
        
        message.reply.assert_called_with("Напоминание удалено")
        mock_log.assert_any_call('info', f'Команда /delete_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Напоминание с ID 1 удалено для пользователя: {message.from_user.id}')


@pytest.mark.asyncio
async def test_handle_delete_reminder_invalid_number() -> None:
    """Тест для обработки попытки удаления напоминания с неверным номером.

    Проверяет, что функция отправляет сообщение об ошибке, если номер напоминания неверен.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/delete_reminder 3"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders:
        
        mock_get_all_reminders.return_value = reminders
        
        await handle_delete_reminder(message)
        
        message.reply.assert_called_with("Пожалуйста, укажите корректный номер напоминания.")
        mock_log.assert_any_call('info', f'Команда /delete_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Ошибка: неверный номер напоминания для пользователя: {message.from_user.id}. Ошибка: Номер напоминания вне диапазона.')


@pytest.mark.asyncio
async def test_handle_delete_reminder_exception() -> None:
    """Тест для обработки исключений при удалении напоминания.

    Проверяет, что функция отправляет сообщение об ошибке, если возникает исключение.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/delete_reminder 1"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders, \
         patch('bot.handlers.user_handlers.delete_reminder', new_callable=AsyncMock) as mock_delete_reminder:
        
        mock_get_all_reminders.return_value = reminders
        mock_delete_reminder.side_effect = Exception("Unexpected error")
        
        await handle_delete_reminder(message)
        
        message.reply.assert_called_with("Произошла ошибка при удалении напоминания.")
        mock_log.assert_any_call('info', f'Команда /delete_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Произошла ошибка для пользователя: {message.from_user.id}. Ошибка: Unexpected error')