import os
import constants
from typing import List

output_path = constants.output_directory
input_path = constants.input_directory

def verify_output_folder() -> None:
    """Verifies output folder is present and creates it if necessary."""
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

def generate_output_file_location(file: str) -> str:
    """Generates the correct file location in the output folder for a given filename."""
    return output_path + '\\' + file

def files_not_converted() -> List[str]:
    files: List[str] = []
    return files