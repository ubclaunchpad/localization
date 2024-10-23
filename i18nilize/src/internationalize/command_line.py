#from src.internationalize.helpers import add_language
import json
import argparse
from i18nilize.src.internationalize.helpers import add_language

def cli():
    # initialize the parser
    parser = argparse.ArgumentParser(description="internationalization for translation")
    subparsers = parser.add_subparsers(dest='command')

    # sub parser for add_language
    add_lang_parser = subparsers.add_parser('add-language')
    add_lang_parser.add_argument('language')

    # the subparser is used because different CLIs use a different amount of inputs

    args = parser.parse_args()

    # depending on the command, do different things
    if args.command == 'add-language':
        add_language(args.language)
    else:
        print("Invalid command")

cli()