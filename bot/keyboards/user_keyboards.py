from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_main_kb() -> ReplyKeyboardMarkup:
    """Создать и вернуть основную клавиатуру для бота.

    Эта функция создает клавиатуру с одной кнопкой "Список моих напоминаний".
    Клавиатура адаптируется к размеру экрана.

    Возвращает:
        ReplyKeyboardMarkup: Объект клавиатуры с кнопками.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_we = KeyboardButton('Список моих напоминаний')
    keyboard.add(btn_we)
    return keyboard