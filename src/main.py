from src.driver.driver_handler import config_driver, download_songs
from src.utils.logger_config import setup_logger
from src.utils.song_files_handler import get_input_file_names, move_songs_to_output_dir
from src.utils.args_handler import get_args
from src.params import IS_HIDDEN_RUN


# TODO: fix missing some songs during the download
def main():
    """Downloads a list of songs, where the input is a directory of .txt files containing \n separated names of songs
    Expects the input to be in the directory SongDownloader/input as a set of .txt files, containing one song name
    in a row

    Currently downloads everything into 'C:\Users\GoMaN\Downloads'

    for WSL:
        PYTHONPATH=. python3 src/main.py

    for Windows:
        set PYTHONPATH=.
        python src.main.py

    """
    input_dir, output_dir = get_args()

    setup_logger()

    songs_names = get_input_file_names(input_dir_path=input_dir)

    driver = config_driver(is_hidden_run=IS_HIDDEN_RUN)

    song_file_names = download_songs(driver=driver, songs=songs_names)

    move_songs_to_output_dir(song_file_names=song_file_names, output_dir=output_dir)

    driver.quit()


if __name__ == "__main__":
    main()
