import shutil
from pathlib import Path


def is_file_exist(downloaded_file_path: Path | str) -> bool:
    path = Path(downloaded_file_path)
    return path.is_file()


def remove_dir_if_exist(download_dir):
    path = Path(download_dir)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
