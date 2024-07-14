import os
import constants
from typing import List
import configparser

output_path = constants.output_directory
input_path = constants.input_directory

def verify_output_folder() -> None:
    """Verifies output folder is present and creates it if necessary."""
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

def generate_output_file_location(file: str) -> str:
    """Generates the correct file location in the output folder for a given filename."""
    return os.path.join(output_path, file)

def files_not_converted() -> List[str]:
    files: List[str] = []
    return files

def current_path() -> str:
    return os.getcwd()

def check_for_ini_file() -> bool:
    return os.path.isfile(os.path.join(current_path(),constants.ini_file))

def ini_file_has_output() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "output")

def ini_file_has_input() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "input")

def has_valid_ini_file():
    return check_for_ini_file() and ini_file_has_input() and ini_file_has_input()

def create_ini_file(input_folder: str, output_folder:str) -> None:
    config = configparser.ConfigParser()
    config['IO'] = {'input': input_folder, 'output': output_folder}
    with open(os.path.join(current_path(),constants.ini_file), 'w') as configfile:
        config.write(configfile)