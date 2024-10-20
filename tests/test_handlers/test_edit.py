import pytest
from unittest.mock import AsyncMock, patch
from bot.handlers.user_handlers import handle_edit_reminder

@pytest.mark.asyncio
async def test_handle_edit_reminder() -> None:
    """Тест для обработки редактирования напоминания.

    Проверяет, что функция корректно обновляет напоминание и отправляет ответ пользователю.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/edit_reminder 1 Новый текст напоминания 2024-10-25 14:30:00"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders, \
         patch('bot.handlers.user_handlers.update_reminder', new_callable=AsyncMock) as mock_update_reminder:
        
        mock_get_all_reminders.return_value = reminders
        mock_update_reminder.return_value = "Напоминание обновлено"
        
        await handle_edit_reminder(message)
        
        message.reply.assert_called_with("Напоминание обновлено")
        mock_log.assert_any_call('info', f'Команда /edit_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Напоминание с ID 1 обновлено для пользователя: {message.from_user.id}')


@pytest.mark.asyncio
async def test_handle_edit_reminder_invalid_number() -> None:
    """Тест для обработки попытки редактирования напоминания с неверным номером.

    Проверяет, что функция отправляет сообщение об ошибке, если номер напоминания неверен.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/edit_reminder 3 Новый текст напоминания 2024-10-25 14:30:00"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders:
        
        mock_get_all_reminders.return_value = reminders
        
        await handle_edit_reminder(message)
        
        message.reply.assert_called_with("Пожалуйста, укажите корректный номер напоминания, новый текст и дату.")
        mock_log.assert_any_call('info', f'Команда /edit_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Ошибка: Номер напоминания вне диапазона. для пользователя: {message.from_user.id}')


@pytest.mark.asyncio
async def test_handle_edit_reminder_exception() -> None:
    """Тест для обработки исключений при редактировании напоминания.

    Проверяет, что функция отправляет сообщение об ошибке, если возникает исключение.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/edit_reminder 1 Новый текст напоминания 2024-10-25 14:30:00"

    reminders = [{'id': 1, 'text': 'Напоминание 1'}, {'id': 2, 'text': 'Напоминание 2'}]

    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.get_all_reminders', new_callable=AsyncMock) as mock_get_all_reminders, \
         patch('bot.handlers.user_handlers.update_reminder', new_callable=AsyncMock) as mock_update_reminder:
        
        mock_get_all_reminders.return_value = reminders
        mock_update_reminder.side_effect = Exception("Unexpected error")
        
        await handle_edit_reminder(message)
        
        message.reply.assert_called_with("Произошла ошибка при редактировании напоминания.")
        mock_log.assert_any_call('info', f'Команда /edit_reminder выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Произошла ошибка для пользователя: {message.from_user.id}. Ошибка: Unexpected error')