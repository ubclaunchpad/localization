import setuptools 
from setuptools import find_packages

setuptools.setup(
    name='i18nilize',
    version='1.0',
    packages=find_packages(),
    author='Brian Park',
    entry_points = {
        'console_scripts': ['i18nilize=i18nilize.src.internationalize.command_line:cli'],
    },
)