import os

from src.internationalize import globals
from src.internationalize.diffing_processor import DiffingProcessor


def setup_package():
    try:
        setup_files_exist(globals.ROOT_DIRECTORY)
    except FileExistsError as err:
        print("ERROR:", err)
        return

    dp = DiffingProcessor(globals.LANGUAGES_DIR)
    dp.setup()

    print("i18nilize setup complete.")


def setup_files_exist(root_directory):
    diff_state_directory = os.path.join(root_directory, "diff_state")
    if os.path.exists(diff_state_directory):
        raise FileExistsError(
            "DIFF_STATE directory already exists. Delete the directory to re-run setup."
        )
