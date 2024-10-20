import logging

class BotLogger:
    """Логгер для бота, который записывает сообщения в указанный файл.

    Атрибуты:
        logger (logging.Logger): Объект логгера для записи логов.
    """

    def __init__(self, log_file: str) -> None:
        """Инициализировать BotLogger.

        Аргументы:
            log_file (str): Имя файла для записи логов.
        """
        self.logger = logging.getLogger("bot_logger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, level: str, message: str) -> None:
        """Записать сообщение в лог с заданным уровнем.

        Аргументы:
            level (str): Уровень логирования ('info' или 'error').
            message (str): Сообщение для записи в лог.
        """
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)

logger = BotLogger('bot.log')