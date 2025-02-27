import json
import os

TARGET_DIRECTORIES = [".git", ".venv", "venv", "env", ".i18nilize"]


def get_project_root_directory(config_file_path):
    loaded_root_directory = load_root_directory_from_config(config_file_path)
    if loaded_root_directory:
        return loaded_root_directory

    found_root_directory = find_project_root_directory()
    if found_root_directory:
        save_project_root_directory(config_file_path, found_root_directory)
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
        for target_directory in TARGET_DIRECTORIES:
            target_directory_path = os.path.join(current_path, target_directory)
            target_directory_exists = os.path.isdir(target_directory_path)

            if target_directory_exists:
                return current_path

        current_path = parent_path

    return None


def save_project_root_directory(config_file_path, root_directory):
    config = load_existing_config(config_file_path)
    config["project_root_directory"] = root_directory
    save_config(config_file_path, config)


def load_root_directory_from_config(config_file_path):
    config = load_existing_config(config_file_path)
    root_directory = config.get("project_root_directory")
    return root_directory


def load_existing_config(config_file_path):
    config = {}

    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as f:
            config = json.load(f)

    return config


def save_config(config_file_path, config):
    with open(config_file_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
