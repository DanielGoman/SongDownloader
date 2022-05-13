import time

from src.driver.driver_handler import config_driver, download_songs
from src.utils.logger_config import setup_logger
from src.utils.song_files_handler import get_input_file_names, wait_till_download_is_finished
from params import CONVERTER_URL, INPUT_DIR_PATH


def main():
    setup_logger()

    songs_names = get_input_file_names(input_dir_path=INPUT_DIR_PATH)

    driver = config_driver()

    downloaded_song_names = download_songs(driver=driver, songs=songs_names)

    wait_till_download_is_finished(downloaded_song_names=downloaded_song_names)

    time.sleep(5)


if __name__ == "__main__":
    main()
