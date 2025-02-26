# from src.internationalize.helpers import add_language
import argparse
import os

from src.internationalize import globals
from src.internationalize.helpers import (
    add_language,
    add_update_translated_word,
    delete_translation,
)
from src.internationalize.package_setup import setup_package
from src.internationalize.project_root_utils import get_project_root_directory
from src.internationalize.sync_processor import pull_translations, push_translations


def initialize_root_directory():
    try:
        root_directory = get_project_root_directory(globals.CONFIG_FILE_PATH)
        globals.ROOT_DIRECTORY = root_directory
        globals.LANGUAGES_DIR = os.path.join(root_directory, "languages")
    except FileNotFoundError as err:
        print("ERROR:", err)
        exit(1)


def cli():
    initialize_root_directory()

    # initialize the parser
    parser = argparse.ArgumentParser(description="internationalization for translation")
    subparsers = parser.add_subparsers(dest="command")

    # sub parser for add_language
    add_lang_parser = subparsers.add_parser("add-language")
    add_lang_parser.add_argument("language")

    # sub parser for add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("language")
    add_parser.add_argument("original_word")
    add_parser.add_argument("translated_word")

    # sub parser for update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("language")
    update_parser.add_argument("original_word")
    update_parser.add_argument("translated_word")

    # sub parser for delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("language")
    delete_parser.add_argument("original_word")
    delete_parser.add_argument("translated_word")

    # sub parser for pull
    subparsers.add_parser("pull")

    # sub parser for push
    subparsers.add_parser("push")

    # sub parser for setup
    subparsers.add_parser("setup")

    # the subparser is used because different CLIs use a different amount of inputs

    args = parser.parse_args()

    # depending on the command, do different things
    if args.command == "add-language":
        add_language(args.language)
    elif args.command == "add" or args.command == "update":
        add_update_translated_word(
            args.language, args.original_word, args.translated_word
        )
    elif args.command == "delete":
        delete_translation(args.language, args.original_word, args.translated_word)
    elif args.command == "pull":
        pull_translations()
    elif args.command == "push":
        push_translations()
    elif args.command == "setup":
        setup_package()
    else:
        print("Invalid command.")


if __name__ == "__main__":
    cli()
