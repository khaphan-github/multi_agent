# logger_config.py
import logging


class Logger:
    def __init__(self, name="LOGGER", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._configure_handler(level)

    def _configure_handler(self, level):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.propagate = False

    def get_logger(self):
        return self.logger

    @staticmethod
    def log(message, level=logging.INFO, name="LOGGER"):
        logger = logging.getLogger(name)
        if not logger.handlers:  # Ensure the logger is configured
            Logger(name, level)
        logger.log(level, message)

# Usage:
# LoggerConfig.log("This is a log message", logging.WARNING)
