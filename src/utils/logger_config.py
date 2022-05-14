import logging
import os

from src.params import LOGGING_DIR,DEBUG_LOGGER_NAME, INFO_LOGGER_NAME, LOG_MODE

logger = logging.getLogger('__main__')
logger.setLevel(logging.DEBUG)


def setup_logger():
    """
    Configures the logger with 2 handlers: debug, info
    """
    # create logging dir if it doesn't exist
    os.makedirs(LOGGING_DIR, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # setup debug logger
    if DEBUG_LOGGER_NAME is not None:
        debug_log_full_path = os.path.join(LOGGING_DIR, DEBUG_LOGGER_NAME)
        debug_handler = logging.FileHandler(debug_log_full_path, mode=LOG_MODE)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)

    # setup debug logger
    if INFO_LOGGER_NAME is not None:
        info_log_full_path = os.path.join(LOGGING_DIR, INFO_LOGGER_NAME)
        debug_handler = logging.FileHandler(info_log_full_path, mode=LOG_MODE)
        debug_handler.setLevel(logging.INFO)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)
