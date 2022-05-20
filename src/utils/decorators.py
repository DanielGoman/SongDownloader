import time

from src.utils.logger_config import logger
from src.utils.consts import SECONDS_PER_MINUTE


def timer(func):
    """A timer wrapper function, counts the run time of the given function and registers it in the log

    Args:
        func: the function to run and to count the runtime of

    Returns:
        time_wrapper - the decorator function

    """
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
