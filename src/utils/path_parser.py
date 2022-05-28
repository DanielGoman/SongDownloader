import os
from pathlib import Path

from src.params import PROJECT_NAME


def config_relative_dir(target_dir_name: str) -> str:
    curr_path = Path(os.getcwd())
    path_parts = list(curr_path.parts)

    if PROJECT_NAME in path_parts:
        project_dir_idx = path_parts.index(PROJECT_NAME)
        project_dir_path = os.path.join(*path_parts[:project_dir_idx + 1])
        target_dir = os.path.join(project_dir_path, target_dir_name)
        print(f'Located directory: {target_dir}')
        return target_dir
    else:
        print(rf"Project directory '{PROJECT_NAME}' is missing")
        exit(-1)
