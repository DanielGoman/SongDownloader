from src.driver.driver_handler import config_driver, download_songs
from src.utils.logger_config import setup_logger
from src.utils.song_files_handler import get_input_file_names, move_songs_to_output_dir
from src.utils.args_handler import get_args
from src.params import IS_HIDDEN_RUN


def main():
    input_dir, output_dir = get_args()

    setup_logger()

    songs_names = get_input_file_names(input_path=input_dir)

    driver = config_driver(is_hidden_run=IS_HIDDEN_RUN)

    downloaded_songs = download_songs(driver=driver, songs=songs_names)

    move_songs_to_output_dir(song_file_names=downloaded_songs, output_dir=output_dir)

    driver.quit()


if __name__ == "__main__":
    main()
