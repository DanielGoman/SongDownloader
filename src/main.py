from src.driver.driver_handler import config_driver, download_songs
from src.utils.logger_config import setup_logger
from src.utils.song_files_handler import get_input_file_names
from src.params import INPUT_DIR_PATH, IS_HIDDEN_RUN


#TODO: wrap up with a docker
def main():
    """Downloads a list of songs, where the input is a directory of .txt files containing \n separated names of songs
    Expects the input to be in the directory SongDownloader/input as a set of .txt files, containing one song name
    in a row

    """
    setup_logger()

    songs_names = get_input_file_names(input_dir_path=INPUT_DIR_PATH)

    driver = config_driver(is_hidden_run=IS_HIDDEN_RUN)

    download_songs(driver=driver, songs=songs_names)

    driver.quit()


if __name__ == "__main__":
    main()
