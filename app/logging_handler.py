import logging
import os
from logging.handlers import RotatingFileHandler

# In-memory log for the UI:
IN_MEMORY_LOGS = []

def create_logger():
    """
    Creates a logger that writes to logs/shelly-rebooter.log
    and also keeps messages in memory for the UI.
    """
    logger = logging.getLogger("shelly_rebooter")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            "logs/shelly-rebooter.log", maxBytes=5_000_000, backupCount=3
        )
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_format)
        logger.addHandler(console_handler)

    return logger

LOGGER = create_logger()

def add_log(message: str, level=logging.INFO):
    LOGGER.log(level, message)
    IN_MEMORY_LOGS.append(message)
    if len(IN_MEMORY_LOGS) > 200:
        del IN_MEMORY_LOGS[0]
