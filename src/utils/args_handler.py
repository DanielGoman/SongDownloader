import os
import argparse
from pathlib import Path

from src.utils.consts import DEFAULT_DOWNLOADS_DIR_NAME
from src.utils.path_parser import config_relative_dir
from src.params import INPUT_DIR_NAME


def get_args():
    default_input_path = config_relative_dir(INPUT_DIR_NAME)
    default_output_path = os.path.join(Path.home(), DEFAULT_DOWNLOADS_DIR_NAME)

    parser = argparse.ArgumentParser(description='SongDownloader help menu')

    parser.add_argument('--src', required=False, default=default_input_path, type=str,
                        help='path to the input directory')
    parser.add_argument('--dest', required=False, default=default_output_path, type=str,
                        help='path to the output directory')

    args = parser.parse_args().__dict__

    return args['src'], args['dest']
