import customtkinter as ctk
import functionality.helpers.file_utils as file_utils
import functionality.pinpoint_centre as pinpoint_centre
import functionality.analyse_cell_direction as direction_analysis
import functionality.configuration as configuration
import functionality.auto_pinpoint_centre as auto_pinpoint_centre
from typing import Any
import functionality.constants.constants as constants
import time

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("green")

def update_ui(frame: Any, show_buttons=True):

    is_configured = has_configuration()

    # clean ui
    for widget in frame.winfo_children():
        widget.destroy()
    
    if show_buttons:
        if is_configured:
            ctk.CTkButton(frame, text=f"Pinpoint Centre ({file_utils.files_not_converted_count()})", command= lambda: pinpoint_centre_image(frame=frame)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="Analyse", command= lambda: analyse_cell_direction(frame=frame)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="Configuration", command= lambda: configure_app(frame=frame, show_configuration=True)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="BETA - Auto analysis", command= lambda: auto_analysis(frame=frame)).pack(pady=5, padx=10)
        else:
            ctk.CTkButton(frame, text="Configure", command= lambda: configure_app(frame=frame, show_configuration=True)).pack(pady=5, padx=10)


# --- Helper Functions ---

def has_configuration():
    """Check wether cell_analyser.ini exists and is valid"""
    return file_utils.has_valid_ini_file()

def pinpoint_centre_image(frame: Any):
    update_ui(frame=frame, show_buttons=False)
    pinpoint_centre.run()
    update_ui(frame=frame)

def auto_analysis(frame: Any):
    update_ui(frame=frame, show_buttons=False)
    auto_pinpoint_centre.run()
    direction_analysis.run()
    update_ui(frame=frame)

def analyse_cell_direction(frame: Any):
    start_time = time.time()
    update_ui(frame=frame, show_buttons=False)
    direction_analysis.run()
    update_ui(frame=frame)
    end_time = time.time()
    duration = round(end_time - start_time)
    show_popup('Analysis done!', f'Analysis took {duration} seconds.')

def entry_new_value(entry: ctk.CTkEntry, value: str):
    entry.delete(0, 'end') 
    entry.insert(0, value)

def show_popup(title, text):
    dialog = ctk.CTkInputDialog(
        text=text, 
        title=title
    )
    dialog.get_input()  # Wait for the user to dismiss the dialog

def configure_app(frame: Any, show_configuration: bool = False):
    """Creates ini file for the configuration of the application"""
    update_ui(frame=frame, show_buttons=False)

    ctk.CTkLabel(frame, text="Input Folder", width=360).pack(pady=5, padx=10)
    input_folder_entry = ctk.CTkEntry(frame, width=360)
    input_folder_entry.pack(pady=5, padx=10)
    if(show_configuration):
        entry_new_value(input_folder_entry, configuration.get_input_path())

    ctk.CTkLabel(frame, text="Output Folder", width=360).pack(pady=5, padx=10)
    output_folder_entry = ctk.CTkEntry(frame, width=360)
    output_folder_entry.pack(pady=5, padx=10)
    if(show_configuration):
        entry_new_value(output_folder_entry, configuration.get_output_path())

    ctk.CTkLabel(frame, text="Analysis Folder", width=360).pack(pady=5, padx=10)
    analysis_folder_entry = ctk.CTkEntry(frame, width=360)
    analysis_folder_entry.pack(pady=5, padx=10)
    if(show_configuration):
        entry_new_value(analysis_folder_entry, configuration.get_analysis_path())

    ctk.CTkLabel(frame, text="Separator", width=360).pack(pady=5, padx=10)
    separator_value = ctk.CTkComboBox(frame, width=360, values=[constants.separator_comma, constants.separator_point])
    separator_value.pack(pady=5, padx=10)
    if(show_configuration):
        separator_value.set(configuration.get_separator())

    ctk.CTkButton(frame, text="Cancel", command=lambda: update_ui(frame=frame)).pack(pady=5)
    ctk.CTkButton(frame, text="Save", command=lambda: save_configuration(frame, input_folder_entry, output_folder_entry, analysis_folder_entry, separator_value)).pack(pady=10)

def save_configuration(frame: Any, input_folder_entry, output_folder_entry, analysis_folder_entry, separator_entry):
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    analysis_folder = analysis_folder_entry.get()
    separator = separator_entry.get()
    configuration.save_to_configuration(input_folder, output_folder, analysis_folder, separator)

    update_ui(frame=frame, show_buttons=True)

def main():
    root = ctk.CTk()
    root.title("Analysis App")
    root.geometry("720x480")

    # Title
    ctk.CTkLabel(root, text="Welcome to the polarity analysis App").pack(pady=10)

    frame = ctk.CTkFrame(root)
    frame.pack()

    update_ui(frame=frame)

    root.mainloop()
    
if __name__ == "__main__":
    main()
