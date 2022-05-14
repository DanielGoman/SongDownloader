import os
import time
from typing import List

from src.utils.logger_config import logger
from src.utils.consts import SONG_FILE_FORMAT, TIME_DELTA_TILL_NEXT_DOWNLOADS_CHECK
from src.params import DOWNLOADS_DIR_PATH


def get_input_file_names(input_dir_path: str) -> List[str]:
    """Returns the names of the songs to download

    Args:
        input_dir_path: path to the directory of the input files

    Returns:
        song_names - list of the song names to download

    """
    song_names = []
    if os.path.isdir(input_dir_path):
        song_files = os.listdir(input_dir_path)
        for song_file in song_files:
            song_file_path = os.path.join(input_dir_path, song_file)
            with open(song_file_path) as input_file:
                file_song_names = input_file.readlines()
                file_song_names = [song_name.replace('\n', '') for song_name in file_song_names]
            song_names += file_song_names
        logger.info(f'Found {len(song_names)} songs')
    else:
        logger.debug(f"Input path '{input_dir_path}' is not a dir")
        exit()

    return song_names


def format_song_name(song_name: str) -> str:
    """Turns the first letter of each word to uppercase

    Args:
        song_name: the original names of the songs

    Returns:
        the name of the song where the first letter of each word is in uppercase
    """
    return song_name.title()


def wait_till_download_is_finished(downloaded_song_names: List[str]):
    """Waits for all the files to be fully downloaded before allowing the program to proceed and shut down

    Args:
        downloaded_song_names: list of the names of all the song files expected to be found in the downloads directory

    """
    song_file_names = [song_name + '.' + SONG_FILE_FORMAT for song_name in downloaded_song_names]
    song_count = len(song_file_names)
    num_remaining = song_count

    while len(song_file_names) > 0:
        downloads_list = os.listdir(DOWNLOADS_DIR_PATH)
        downloaded_songs_paths = [os.path.join(DOWNLOADS_DIR_PATH, file_name) for file_name in downloads_list]
        for index_in_expected_list, song_file_name in enumerate(song_file_names):
            if song_file_name in downloads_list:
                index_in_downloads_list = downloads_list.index(song_file_name)
                if os.path.isfile(downloaded_songs_paths[index_in_downloads_list]):
                    song_file_names.pop(index_in_expected_list)

        new_num_remaining = len(song_file_names)
        if new_num_remaining < num_remaining:
            logger.info(f'Finished downloading {song_count - new_num_remaining}/{song_count} songs')
            num_remaining = new_num_remaining

        time.sleep(TIME_DELTA_TILL_NEXT_DOWNLOADS_CHECK)
