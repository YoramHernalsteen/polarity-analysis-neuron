import customtkinter as ctk
import functionality.helpers.file_utils as file_utils
import functionality.pinpoint_centre as pinpoint_centre
import functionality.analyse_cell_direction as direction_analysis
import functionality.configuration as configuration
import functionality.auto_pinpoint_centre as auto_pinpoint_centre
from typing import Any

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("green")

def update_ui(frame: Any, show_buttons=None):
    if show_buttons is None:
        show_buttons = True

    is_configured = has_configuration()

    # clean ui
    for widget in frame.winfo_children():
        widget.destroy()

    if show_buttons:
        if is_configured:
            ctk.CTkButton(frame, text=f"Pinpoint Centre ({file_utils.files_not_converted_count()})", command= lambda: pinpoint_centre_image(frame=frame)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="Analyse", command= lambda: analyse_cell_direction(frame=frame)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="Configuration", command= lambda: display_configuration(frame=frame)).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="BETA - Auto analysis", command= lambda: auto_analysis(frame=frame)).pack(pady=5, padx=10)
        else:
            ctk.CTkButton(frame, text="Configure", command= lambda: configure_app(frame=frame)).pack(pady=5, padx=10)


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
    update_ui(frame=frame, show_buttons=False)
    direction_analysis.run()
    update_ui(frame=frame)

def analyze():
    """Your data analysis logic."""
    pass

def configure_app(frame: Any):
    """Creates ini file for the configuration of the application"""
    update_ui(frame=frame, show_buttons=False)

    ctk.CTkLabel(frame, text="Input Folder:").pack(pady=5, padx=10)
    input_folder_entry = ctk.CTkEntry(frame)
    input_folder_entry.pack(pady=5, padx=10)

    ctk.CTkLabel(frame, text="Output Folder:").pack(pady=5, padx=10)
    output_folder_entry = ctk.CTkEntry(frame)
    output_folder_entry.pack(pady=5, padx=10)

    ctk.CTkLabel(frame, text="Analysis Folder:").pack(pady=5, padx=10)
    analysis_folder_entry = ctk.CTkEntry(frame)
    analysis_folder_entry.pack(pady=5, padx=10)

    ctk.CTkButton(frame, text="Cancel", command=lambda: update_ui(frame=frame)).pack(pady=5)
    ctk.CTkButton(frame, text="Save", command=lambda: save_configuration(frame, input_folder_entry, output_folder_entry, analysis_folder_entry)).pack(pady=10)

def save_configuration(frame: Any, input_folder_entry, output_folder_entry, analysis_folder_entry):
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    analysis_folder = analysis_folder_entry.get()
    configuration.save_to_configuration(input_folder, output_folder, analysis_folder)

    update_ui(frame=frame, show_buttons=True)

def display_configuration(frame: Any):
    update_ui(frame=frame, show_buttons=False)

    input_label = ctk.CTkLabel(master=frame, text=f"INPUT: {configuration.get_input_path()}")
    input_label.pack()

    output_label = ctk.CTkLabel(master=frame, text=f"OUTPUT: {configuration.get_output_path()}")
    output_label.pack()

    analysis_label = ctk.CTkLabel(master=frame, text=f"ANALYSIS: {configuration.get_analysis_path()}")
    analysis_label.pack()

    ctk.CTkButton(frame, text="Menu", command= lambda: update_ui(frame=frame)).pack(pady=5)


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
