import argparse

from . import globals
from .helpers import (
    add_language,
    add_update_translated_word,
    delete_translation,
)
from .package_init_utils import (
    initialize_root_directory,
    setup_package,
    validate_required_directories,
)
from .sync_processor import pull_translations, push_translations
from .diffing_processor import DiffingProcessor
from .api_helpers import relinquish_writer_permissions, request_writer_permissions


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

    # sub parser for relinquishing writer permissions
    subparsers.add_parser("relinquish-writer")

    # sub parser for requesting writer permissions
    subparsers.add_parser("request-writer")

    # the subparser is used because different CLIs use a different amount of inputs

    args = parser.parse_args()

    # depending on the command, do different things
    if args.command == "setup":
        setup_package()
        return

    validate_required_directories()

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
    elif args.command == "relinquish-writer":
        relinquish_writer_permissions()
    elif args.command == "request-writer":
        request_writer_permissions()
    else:
        print("Invalid command.")


if __name__ == "__main__":
    cli()
