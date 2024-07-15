import os
import functionality.constants.constants as constants
from typing import List
import configparser

def get_ini_value(section: str, option: str) -> str:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.get(section=section, option=option)

def get_dir_from_ini(section: str, option: str) -> str:
    return os.path.normpath(get_ini_value(section=section, option=option))

def ini_file_valid_dir_value(section: str, option: str) -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    if(not config.has_option(section=section, option=option)):
        return False
    
    if(config.get(section=section, option=option) == ''):
        return False
    
    return os.path.exists(os.path.normpath(config.get(section=section, option=option)))

def output_path() -> str:
    return get_dir_from_ini('IO', 'output')

def input_path() -> str:
    return get_dir_from_ini('IO', 'input')

def analysis_path() -> str:
    return get_dir_from_ini('IO', 'analysis')

def verify_output_folder() -> None:
    """Verifies output folder is present and creates it if necessary."""
    if not os.path.exists(output_path()):
        os.makedirs(output_path(), exist_ok=True)

def generate_output_file_location(file: str) -> str:
    """Generates the correct file location in the output folder for a given filename."""
    return os.path.join(output_path(), file)

def current_path() -> str:
    return os.getcwd()

def check_for_ini_file() -> bool:
    return os.path.isfile(os.path.join(current_path(),constants.ini_file))

def ini_file_has_output() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "output") and ini_file_valid_dir_value("IO", "output")

def ini_file_has_input() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "input") and ini_file_valid_dir_value("IO", "input")

def ini_file_has_analysis() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "analysis") and ini_file_valid_dir_value("IO", "analysis")

def has_valid_ini_file():
    return check_for_ini_file() and ini_file_has_output() and ini_file_has_input() and ini_file_has_analysis()

def create_ini_file(input_folder: str, output_folder:str, analysis_folder:str) -> None:
    config = configparser.ConfigParser()
    config['IO'] = {'input': input_folder, 'output': output_folder, 'analysis' : analysis_folder}
    with open(os.path.join(current_path(),constants.ini_file), 'w') as configfile:
        config.write(configfile)
        
def files_not_converted() -> List[str]:
    """Compares files in input and output folders and returns those in the input but not the output."""
    missing_files = []
    
    input_folder = input_path()
    output_folder = output_path()
    
    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename)
        if os.path.isfile(input_file) and not os.path.isfile(output_file):
            missing_files.append(input_file)
    
    return missing_files

def files_not_converted_count() -> int:
    """Compares files in input and output folders and returns the number of those in the input but not the output."""
    return len(files_not_converted())