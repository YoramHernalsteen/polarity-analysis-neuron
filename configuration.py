import file_utils

def save_to_configuration(input_folder: str, output_folder: str, analysis_folder: str):
    file_utils.create_ini_file(input_folder=input_folder, output_folder=output_folder, analysis_folder=analysis_folder)
    
def get_output_path() -> str:
    return file_utils.output_path()

def get_input_path() -> str:
    return file_utils.input_path()

def get_analysis_path() -> str:
    return file_utils.analysis_path()