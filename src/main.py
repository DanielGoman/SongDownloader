import time

from src.driver.driver_handler import config_driver, download_songs
from src.utils.logger_config import setup_logger
from src.utils.song_files_handler import wait_till_download_is_finished
from params import CONVERTER_URL


def main():
    setup_logger()

    driver = config_driver(converter_url=CONVERTER_URL)

    downloaded_song_names = download_songs(driver=driver, songs=['The Wreckage - Breaking Through'])

    wait_till_download_is_finished(downloaded_song_names=downloaded_song_names)

    time.sleep(5)


if __name__ == "__main__":
    main()
