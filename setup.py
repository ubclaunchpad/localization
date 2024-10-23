import setuptools 
from setuptools import find_packages

# setup file for the command line
# before testing, do the following command:
#  pip install -e
# within the virtual environment, this will enable you to use i18nilize CLI
setuptools.setup(
    # package name
    name='i18nilize',

    # arbitrary version #
    version='1.0',

    # downloads the necessary packages (ex. json)
    packages=find_packages(),

    # directs the script towards the function located in that file
    entry_points = {
        'console_scripts': ['i18nilize=i18nilize.src.internationalize.command_line:cli'],
    },
)