import os
from typing import List

from src.utils.logger_config import logger


def get_input_file_names(input_dir_path: str) -> List[str]:
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
        pass

    return song_names


def format_song_name(song: str) -> str:
    return song


def wait_till_download_is_finished(downloaded_song_names: List[str]):
    pass
