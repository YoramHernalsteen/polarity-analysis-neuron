import customtkinter as ctk
import functionality.helpers.file_utils as file_utils
import functionality.analyse_cell_direction as analysis
import functionality.configuration as configuration
import functionality.constants.constants as constants
import functionality.pinpoint_centre as pinpoint_centre
import functionality.auto_pinpoint_centre as auto_pinpoint_centre
import app.helpers.app_helper as app_helper
import time
import threading

class App(ctk.CTk):
    configured = False
    menu_frame = None
    action_frame = None
    configuration_frame = None

    def __init__(self):
        super().__init__()

        self.configured = file_utils.has_valid_ini_file()
        self.title("Analysis App")
        self.geometry("720x480")

        # Title
        ctk.CTkLabel(self, text="Welcome to the polarity analysis App").pack(pady=10)

        self.render('menu')
    
    def display_configuration_frame(self):
        if self.configuration_frame is None or not self.configuration_frame.winfo_exists():
            self.configuration_frame = ctk.CTkFrame(self)

        self.configuration_frame.pack()

        show_configuration = True

        ctk.CTkLabel(self.configuration_frame, text="Input Folder", width=360).pack(pady=5, padx=10)
        input_folder_entry = ctk.CTkEntry(self.configuration_frame, width=360)
        input_folder_entry.pack(pady=5, padx=10)
        if(show_configuration):
            app_helper.entry_new_value(input_folder_entry, configuration.get_input_path())
            input_folder_entry.focus_set() ## otherwise it has a weird issue with focus

        ctk.CTkLabel(self.configuration_frame, text="Output Folder", width=360).pack(pady=5, padx=10)
        output_folder_entry = ctk.CTkEntry(self.configuration_frame, width=360)
        output_folder_entry.pack(pady=5, padx=10)
        if(show_configuration):
            app_helper.entry_new_value(output_folder_entry, configuration.get_output_path())

        ctk.CTkLabel(self.configuration_frame, text="Analysis Folder", width=360).pack(pady=5, padx=10)
        analysis_folder_entry = ctk.CTkEntry(self.configuration_frame, width=360)
        analysis_folder_entry.pack(pady=5, padx=10)
        if(show_configuration):
            app_helper.entry_new_value(analysis_folder_entry, configuration.get_analysis_path())

        ctk.CTkLabel(self.configuration_frame, text="Separator", width=360).pack(pady=5, padx=10)
        separator_value = ctk.CTkComboBox(self.configuration_frame, width=360, values=[constants.separator_comma, constants.separator_point])
        separator_value.pack(pady=5, padx=10)
        if(show_configuration):
            separator_value.set(configuration.get_separator())

        ctk.CTkButton(self.configuration_frame, text="Cancel", command=lambda: self.render('menu')).pack(pady=5)
        ctk.CTkButton(self.configuration_frame, text="Save", command=lambda: self.save_configuration(input_folder_entry, output_folder_entry, analysis_folder_entry, separator_value)).pack(pady=10)
    
    def save_configuration(self, input_folder_entry, output_folder_entry, analysis_folder_entry, separator_entry):
        app_helper.save_configuration(input_folder_entry, output_folder_entry, analysis_folder_entry, separator_entry)
        self.render('menu')

    def display_menu_frame(self):
        if self.menu_frame is None or not self.menu_frame.winfo_exists():
            self.menu_frame = ctk.CTkFrame(self)
        
        self.menu_frame.pack()

        if self.configured:
            ctk.CTkButton(self.menu_frame, text=f"Pinpoint Centre ({file_utils.files_not_converted_count()})", command= lambda: self.start_pinpoint_centre_image()).pack(pady=5, padx=10)
            ctk.CTkButton(self.menu_frame, text=f"Analyse ({file_utils.files_not_analysed_count()})", command= lambda: self.start_analysis()).pack(pady=5, padx=10)
            ctk.CTkButton(self.menu_frame, text="Analyse All", command= lambda: self.start_analysis(analyse_all=True)).pack(pady=5, padx=10)
            ctk.CTkButton(self.menu_frame, text="Configuration", command= lambda: self.render('configuration')).pack(pady=5, padx=10)
            ctk.CTkButton(self.menu_frame, text="BETA - Auto analysis", command= lambda: self.start_auto_analysis()).pack(pady=5, padx=10)
        else:
            ctk.CTkButton(self.menu_frame, text="Configure", command= lambda: self.render('configuration')).pack(pady=5, padx=10)

    def start_pinpoint_centre_image(self):
        self.pinpoint_centre()

    def start_auto_analysis(self):
        self.render('auto_analyse')
        x = threading.Thread(target=self.auto_analyse)
        x.start()

    def start_analysis(self, analyse_all: bool = False):
        self.render('analyse')
        x = threading.Thread(target=self.analyse, args=(analyse_all,))
        x.start()
    
    def analyse(self, analyse_all: bool):
        analysis.run(analyse_all)
        self.render('menu')

    def pinpoint_centre(self):
        pinpoint_centre.run()
        self.render('menu')

    def auto_analyse(self):
        auto_pinpoint_centre.run()
        analysis.run(True)
        self.render('menu')
        
    def display_analyse_frame(self):
        self.display_action_frame('Analysing...')

    def display_auto_analyse_frame(self):
        self.display_action_frame('Auto detecting centre of neurons and analysing...')
    
    def display_pinpoint_centre_frame(self):
        self.display_action_frame('Pinpoint centre of neurons...')

    def display_action_frame(self, action: str):
        if self.action_frame is None or not self.action_frame.winfo_exists():
            self.action_frame = ctk.CTkFrame(self)
        
        self.action_frame.pack(pady=5, padx=10)
        ctk.CTkLabel(self.action_frame, text=f"{action}").pack(pady=10)

    def render(self, frame:str):
        for widget in self.winfo_children():
            widget.destroy()
        
        match frame:
            case 'menu':
                self.display_menu_frame()
            case 'analyse':
                self.display_analyse_frame()
            case 'configuration':
                self.display_configuration_frame()
            case 'pinpoint_centre':
                self.display_pinpoint_centre_frame()
            case 'auto_analyse':
                self.display_auto_analyse_frame()
                
        

