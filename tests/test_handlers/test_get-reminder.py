import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from bot.handlers.user_handlers import get_reminder_text

@pytest.mark.asyncio
async def test_get_reminder_text() -> None:
    """Тест для получения текста напоминания.

    Проверяет, что функция корректно анализирует напоминание, отправляет сообщения пользователю
    и устанавливает напоминание в Redis.
    """
    message = AsyncMock()
    message.from_user.id = 12345
    
    redis_pool = AsyncMock()
    future_date = datetime.now() + timedelta(minutes=5)
    text_remind = "Напоминание"
    date_str = future_date.strftime("%Y-%m-%d")
    time_str = future_date.strftime("%H:%M:%S")
    
    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.analyze_reminder_handlers', new_callable=AsyncMock) as mock_analyze_reminder_handlers, \
         patch('bot.handlers.user_handlers.set_info_remind', new_callable=AsyncMock) as mock_set_info_remind, \
         patch('bot.handlers.user_handlers.datetime') as mock_datetime:
        
        mock_analyze_reminder_handlers.return_value = (text_remind, future_date, date_str, time_str)
        mock_datetime.now.return_value = datetime.now()
        
        await get_reminder_text(message, redis_pool)
        
        message.answer.assert_any_call("Идёт анализ вашего напоминания...")
        message.answer.assert_any_call(f'📝 Ваше напоминание: "{text_remind}"\n🗓 Дата: {date_str} \n⏰ Время: {time_str}')
        redis_pool.enqueue_job.assert_called_once_with("send_message", _defer_until=future_date, chat_id=message.from_user.id, text=f"Пришло время:\n{text_remind}")
        mock_set_info_remind.assert_called_once_with(message=message)
        
        mock_log.assert_any_call('info', f'Получение текста напоминания от пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Отправка сообщения об анализе напоминания для пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Напоминание установлено для пользователя: {message.from_user.id}, текст: "{text_remind}", время: {future_date}')


@pytest.mark.asyncio
async def test_get_reminder_text_min_time_error() -> None:
    """Тест для обработки ошибки минимального времени напоминания.
    
    """
    message = AsyncMock()
    message.from_user.id = 12345
    
    redis_pool = AsyncMock()
    past_date = datetime.now() - timedelta(minutes=5)
    text_remind = "Напоминание"
    date_str = past_date.strftime("%Y-%m-%d")
    time_str = past_date.strftime("%H:%M:%S")
    
    with patch('bot.handlers.user_handlers.logger.log') as mock_log, \
         patch('bot.handlers.user_handlers.analyze_reminder_handlers', new_callable=AsyncMock) as mock_analyze_reminder_handlers, \
         patch('bot.handlers.user_handlers.datetime') as mock_datetime:
        
        mock_analyze_reminder_handlers.return_value = (text_remind, past_date, date_str, time_str)
        mock_datetime.now.return_value = datetime.now()
        
        await get_reminder_text(message, redis_pool)
        
        message.answer.assert_any_call("Идёт анализ вашего напоминания...")
        message.answer.assert_any_call("⚠ Минимальное время - 1 минута")
        
        mock_log.assert_any_call('info', f'Получение текста напоминания от пользователя: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Отправка сообщения об анализе напоминания для пользователя: {message.from_user.id}')
        mock_log.assert_any_call('error', f'Попытка установить напоминание через минуту для пользователя: {message.from_user.id}')