import time

from src.utils.logger_config import logger
from src.utils.consts import SECONDS_PER_MINUTE


def timer(func):
    def timer_wrapper(*args, **kwargs):

        logger.info(f'Beginning function {func.__name__}')
        start_time = time.time()

        func(*args, **kwargs)

        end_time = time.time()

        elapsed_time = end_time - start_time
        elapsed_minutes = int(elapsed_time // SECONDS_PER_MINUTE)
        elapsed_seconds = int(elapsed_time % SECONDS_PER_MINUTE)

        logger.info(f'Finished function {func.__name__} in {elapsed_minutes} minutes and {elapsed_seconds} seconds')

    return timer_wrapper
