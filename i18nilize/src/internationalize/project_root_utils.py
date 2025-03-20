import os

TARGET_DIRECTORIES = [".git", ".venv", "venv", "env", ".i18nilize"]


def get_project_root_directory():
    found_root_directory = find_project_root_directory()
    if found_root_directory:
        return found_root_directory

    raise FileNotFoundError(
        "Project root directory could not be found. "
        f"Ensure you are including one of these directories in your root directory: {', '.join(TARGET_DIRECTORIES)}"
    )


def find_project_root_directory(start_path=None):
    if start_path is None:
        start_path = os.getcwd()

    current_path = os.path.abspath(start_path)

    while current_path != (parent_path := os.path.dirname(current_path)):
        # If current_path and parent_path are the same, we've reached the system root directory.
        for target_directory in TARGET_DIRECTORIES:
            target_directory_path = os.path.join(current_path, target_directory)
            target_directory_exists = os.path.isdir(target_directory_path)

            if target_directory_exists:
                return current_path

        current_path = parent_path

    return None
