import customtkinter as ctk
from typing import Any
import functionality.configuration as configuration

def entry_new_value(entry: ctk.CTkEntry, value: str):
    entry.delete(0, 'end') 
    entry.insert(0, value)

def save_configuration(input_folder_entry, output_folder_entry, analysis_folder_entry, separator_entry):
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    analysis_folder = analysis_folder_entry.get()
    separator = separator_entry.get()
    configuration.save_to_configuration(input_folder, output_folder, analysis_folder, separator)