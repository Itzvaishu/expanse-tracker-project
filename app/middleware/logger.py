import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler("logs/expense_tracker.log", maxBytes=1000000, backupCount=5)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
