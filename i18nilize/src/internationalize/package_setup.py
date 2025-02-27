import os

from src.internationalize import globals
from src.internationalize.diffing_processor import DiffingProcessor


def create_directories():
    if setup_directories_exist(globals.ROOT_DIRECTORY):
        raise FileExistsError(
            "The package has already been setup. Delete the diff_state directory to re-run setup."
        )

    dp = DiffingProcessor(globals.LANGUAGES_DIR)
    dp.setup()

    print("i18nilize setup complete.")


def setup_directories_exist(root_directory):
    diff_state_directory = os.path.join(root_directory, "diff_state")
    return os.path.exists(diff_state_directory)
