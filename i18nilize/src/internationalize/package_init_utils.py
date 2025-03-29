import os

from . import globals
from .diffing_processor import DiffingProcessor


def setup_package():
    try:
        create_directories()
    except FileExistsError as err:
        print("Error:", err)
        exit(1)


def create_directories():
    if setup_directories_exist():
        raise FileExistsError(
            "The package has already been setup. Delete the diff_state directory to re-run setup."
        )

    dp = DiffingProcessor(globals.LANGUAGES_DIR)
    dp.setup()

    print("i18nilize setup complete.")


def validate_required_directories():
    if not setup_directories_exist():
        print(
            'Error: i18nilize has not been setup yet. Run "i18nilize setup" to initialize the package.'
        )
        exit(1)


def setup_directories_exist():
    diff_state_directory = os.path.join(globals.ROOT_DIRECTORY, "diff_state")
    return os.path.exists(diff_state_directory)
