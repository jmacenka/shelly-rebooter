import logging
import os
from logging.handlers import RotatingFileHandler

# In-memory log for the UI:
IN_MEMORY_LOGS = []

def load_existing_logs():
    """
    Read the existing log file from disk, store the last 200 lines in IN_MEMORY_LOGS.
    """
    log_path = "logs/shelly-rebooter.log"
    if os.path.isfile(log_path):
        with open(log_path, "r") as f:
            lines = f.readlines()
        # Keep only last 200 lines
        last_lines = lines[-200:]
        for line in last_lines:
            # Remove trailing newlines
            IN_MEMORY_LOGS.append(line.rstrip())

def create_logger():
    """
    Creates a logger that writes to logs/shelly-rebooter.log
    and also keeps messages in memory for the UI.
    Also loads existing logs from disk so the UI can see them.
    """
    logger = logging.getLogger("shelly_rebooter")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        os.makedirs("logs", exist_ok=True)
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

        # Load logs on first creation
        load_existing_logs()

    return logger

LOGGER = create_logger()

def add_log(message: str, level=logging.INFO):
    """
    Log a message to file and also store it in memory for the UI.
    """
    LOGGER.log(level, message)
    IN_MEMORY_LOGS.append(message)
    # Cap in-memory logs at 200 entries
    if len(IN_MEMORY_LOGS) > 200:
        del IN_MEMORY_LOGS[0]
