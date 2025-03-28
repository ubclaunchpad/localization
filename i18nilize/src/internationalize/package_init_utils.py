import os

from src.internationalize import globals
from src.internationalize.diffing_processor import DiffingProcessor
from src.internationalize.project_root_utils import get_project_root_directory


def initialize_root_directory():
    try:
        root_directory = get_project_root_directory()
        globals.ROOT_DIRECTORY = root_directory
        globals.LANGUAGES_DIR = os.path.join(root_directory, "languages")
    except FileNotFoundError as err:
        print("Error:", err)
        exit(1)


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
