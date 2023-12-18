import logging
import locale
import sys

USE_STDOUT = False
USE_FILTER = False
CACHE_LOG_FILENAME = "cache.log"


class CustomFormatter(logging.Formatter):
    """
    Кастомизация цвета сообщения на экране в зависимости от уровня события
    """

    # Цвета для вывода журнала на консоль
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):  # pylint: disable=function-redefined
        """
        Кастомизация формата даты при выводе сообщений на экран
        """
        log_fmt = self.FORMATS.get(record.levelno)
        # Чт 14.12.2023 11:55:10
        formatter = logging.Formatter(log_fmt, datefmt="%a %d.%m.%Y %H:%M:%S")
        return formatter.format(record)


class NoParsingFilter(logging.Filter):
    """
    Фильтрация сообщений по ключевому слову. Используется при запуске внешней программы с параметром -f
    """

    def filter(self, record):
        return "updated" not in record.getMessage()


def startup(name):
    """
    Настройка логгера. Выполняется 1 раз для каждого 'name'
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        locale.setlocale(locale.LC_TIME, locale="ru_RU.utf8")
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler = logging.FileHandler(CACHE_LOG_FILENAME, mode="a")
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        if USE_FILTER:
            logger.addFilter(NoParsingFilter())
        logger.addHandler(handler)
        logger.debug("******* New log session started *******")
        if USE_FILTER:
            logger.debug("Log filtering is enabled.")
        if USE_STDOUT:
            screen_handler = logging.StreamHandler(stream=sys.stdout)
            screen_handler.setFormatter(CustomFormatter())
            logger.addHandler(screen_handler)
            logger.debug("Console output of logs is enabled.")
    return logger
