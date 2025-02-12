import setuptools 
from setuptools import find_packages
from setuptools.command.install import install
import os
import json

CONFIG_FILE = os.path.expanduser("~/.i18nilize_config.json")

def find_project_root(start_path=None):
    if start_path is None:
        start_path = os.getcwd()
    current_path = os.path.abspath(start_path)
    while current_path != os.path.dirname(current_path):  
        if os.path.isdir(os.path.join(current_path, ".git")):
            return current_path  
        current_path = os.path.dirname(current_path) 
    return None 

class OnInstallCommand(install):
    """Custom install command to save installation directory."""
    def run(self):
        install.run(self) 

        install_dir = find_project_root()
        if install_dir is None:
            install_dir = os.getcwd() 

        # Save installation directory
        with open(CONFIG_FILE, "w") as f:
            json.dump({"installation_dir": install_dir}, f)

        print(f"[INFO] Saved installation directory: {install_dir}")

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
    cmdclass={
        'install':OnInstallCommand,
    }
)