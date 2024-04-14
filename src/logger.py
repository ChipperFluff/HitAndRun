import logging
from colorama import Fore, Style, init
from enum import Enum

# Initialize colorama
init(autoreset=True)

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class ColoredFormatter(logging.Formatter):
    """ Custom formatter to add colors to the logging output based on the level. """
    COLORS = {
        LogLevel.DEBUG: Fore.BLUE,
        LogLevel.INFO: Fore.WHITE,
        LogLevel.WARNING: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED,
        LogLevel.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        level_color = self.COLORS.get(LogLevel(record.levelno), Fore.WHITE)
        formatted_record = super().format(record)
        return level_color + formatted_record

class CustomLogger:
    def __init__(self, name, level=LogLevel.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level.value)
        ch = logging.StreamHandler()
        ch.setLevel(level.value)
        formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def set_filter(self, level):
        """ Set the minimum log level for messages. """
        self.logger.setLevel(level.value)
        for handler in self.logger.handlers:
            handler.setLevel(level.value)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

log = CustomLogger('myApp')
debug = log.debug
info = log.info
warning = log.warning
error = log.error
critical = log.critical
