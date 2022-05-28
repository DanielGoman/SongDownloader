import os
import time
import shutil
from typing import List

from src.utils.logger_config import logger
from src.utils.consts import SONG_FILE_FORMAT, TIME_DELTA_TILL_NEXT_DOWNLOADS_CHECK, DOWNLOAD_WAIT_TIMEOUT_PER_FILE
from src.params import DOWNLOADS_DIR_PATH


def get_input_file_names(input_path: str) -> List[str]:
    """Returns the names of the songs to download

    Args:
        input_path: path to the directory of the input files or to a single file

    Returns:
        song_names - list of the song names to download

    """
    song_names = []

    input_path = os.path.abspath(input_path)

    if os.path.isdir(input_path):
        song_files = os.listdir(input_path)
        for song_file in song_files:
            song_file_path = os.path.join(input_path, song_file)
            songs_in_file = read_songs_file(input_path=song_file_path)
            song_names += songs_in_file
    elif os.path.isfile(input_path):
        song_names = read_songs_file(input_path=input_path)

    logger.info(f'Found {len(song_names)} songs')

    return song_names


def read_songs_file(input_path: str) -> List[str]:
    with open(input_path) as input_file:
        file_song_names = input_file.readlines()
        file_song_names = [song_name.replace('\n', '') for song_name in file_song_names]

    return file_song_names


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
    total_timeout_seconds = len(downloaded_song_names) * DOWNLOAD_WAIT_TIMEOUT_PER_FILE

    song_file_names = [song_name + '.' + SONG_FILE_FORMAT for song_name in downloaded_song_names]
    songs_to_be_downloaded = song_file_names.copy()
    song_count = len(song_file_names)
    num_remaining = song_count

    start_time = time.time()
    while len(song_file_names) > 0:
        curr_time = time.time()
        elapsed_seconds = curr_time - start_time
        if elapsed_seconds > total_timeout_seconds:
            logger.info(f'Waiting timeout - waited {int(elapsed_seconds)} seconds')
            break

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

    return songs_to_be_downloaded


def move_songs_to_output_dir(song_file_names: List[str], output_dir: str):
    time.sleep(TIME_DELTA_TILL_NEXT_DOWNLOADS_CHECK)
    if os.path.abspath(DOWNLOADS_DIR_PATH) != os.path.abspath(output_dir):
        song_file_paths = [os.path.join(DOWNLOADS_DIR_PATH, song_file_name) for song_file_name in song_file_names]
        os.makedirs(output_dir, exist_ok=True)

        logger.info(f'Moving songs from default downloads dir to {output_dir}')
        moved_count = 0
        for song_file_name, song_file_path in zip(song_file_names, song_file_paths):
            try:
                shutil.move(src=song_file_path, dst=output_dir)
                logger.info(f'Moved {song_file_name}')
                moved_count += 1
            except OSError as error:
                logger.debug(f'Failed to move {song_file_name} to {output_dir} with error: {str(error)}')

        logger.info(f'Successfully moved {moved_count}/{len(song_file_names)}')
