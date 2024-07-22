import functionality.helpers.file_utils as file_utils

def save_to_configuration(input_folder: str, output_folder: str, analysis_folder: str, seperator: str):
    file_utils.create_ini_file(input_folder=input_folder, output_folder=output_folder, analysis_folder=analysis_folder, separator=seperator)
    
def get_output_path() -> str:
    return file_utils.output_path()

def get_input_path() -> str:
    return file_utils.input_path()

def get_analysis_path() -> str:
    return file_utils.analysis_path()

def get_separator() -> str:
    return file_utils.separator()