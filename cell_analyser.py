import customtkinter as ctk
import file_utils
import pinpoint_centre

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

def update_ui(show_buttons=None):
    if show_buttons is None:
        show_buttons = True

    is_configured = has_configuration()

    # clean ui
    for widget in frame.winfo_children():
        widget.destroy()

    # Create new buttons based on configuration
    if show_buttons:
        if is_configured:
            ctk.CTkButton(frame, text="Pinpoint Centre", command=pinpoint_centre_image).pack(pady=5, padx=10)
            ctk.CTkButton(frame, text="Analyze", command=analyze).pack(pady=5, padx=10)
        else:
            ctk.CTkButton(frame, text="Configure", command=configure_app).pack(pady=5, padx=10)


# --- Helper Functions ---

def has_configuration():
    """Check wether cell_analyser.ini exists and is valid"""
    return file_utils.has_valid_ini_file()

def pinpoint_centre_image():
    pinpoint_centre.run()

def analyze():
    """Your data analysis logic."""
    pass

def configure_app():
    """Your application configuration logic."""
    update_ui(show_buttons=False)
    ctk.CTkLabel(frame, text="Input Folder:").pack(pady=5, padx=10)
    input_folder_entry = ctk.CTkEntry(frame)
    input_folder_entry.pack(pady=5, padx=10)

    ctk.CTkLabel(frame, text="Output Folder:").pack(pady=5, padx=10)
    output_folder_entry = ctk.CTkEntry(frame)
    output_folder_entry.pack(pady=5, padx=10)
    # Save Button
    ctk.CTkButton(frame, text="Cancel", command=update_ui).pack(pady=5)
    ctk.CTkButton(frame, text="Save", command=lambda: save_configuration(input_folder_entry, output_folder_entry)).pack(pady=10)

def save_configuration(input_folder_entry, output_folder_entry):
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    # Call your function to save the configuration
    save_to_configuration(input_folder, output_folder)

    # Update UI to show the main buttons again
    update_ui(show_buttons=True)

def save_to_configuration(input_folder, output_folder):
    file_utils.create_ini_file(input_folder=input_folder, output_folder=output_folder)

# Main Window
root = ctk.CTk()
root.title("Analysis App")
root.geometry("720x480")

# Label
ctk.CTkLabel(root, text="Welcome to the Cell Analysis App").pack(pady=10)

# Frame to hold buttons
frame = ctk.CTkFrame(root)
frame.pack()

# Initial UI Setup
update_ui()

root.mainloop()
