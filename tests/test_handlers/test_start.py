import pytest
from unittest.mock import AsyncMock, patch

from bot.handlers.user_handlers import cmd_start
from bot.keyboards.user_keyboards import get_main_kb

@pytest.mark.asyncio
async def test_start_handler() -> None:
    """Тест для обработки команды /start.

    Проверяет, что функция отправляет приветственное сообщение пользователю 
    и логирует соответствующие действия.
    """
    message = AsyncMock()

    with patch('bot.handlers.user_handlers.logger.log') as mock_log:
        await cmd_start(message)

        start_text = (
            "Привет! Я NudgeNinja, Ваш личный бот-напоминалка. " 
            "Я здесь, чтобы помочь Вам оставаться организованным и не пропустить ни одного важного события.\n\n"
            "Просто напишите мне, что и когда вам нужно вспомнить, и я установлю напоминание для вас ⏰.\n\n"
            "Например, вы можете сказать: “Напомни мне о встрече завтра в 15:00”, и я установлю напоминание на "
            "указанное время и дату 🥷.\n\n"
            "⚠ <b>Если вы не указали дату, я отправлю Вам напоминание сегодня.</b>"
        )

        message.answer.assert_called_with(start_text, parse_mode="html", reply_markup=get_main_kb())
        mock_log.assert_any_call('info', f'Команда /start выполнена пользователем: {message.from_user.id}')
        mock_log.assert_any_call('info', f'Приветственное сообщение отправлено пользователю: {message.from_user.id}')