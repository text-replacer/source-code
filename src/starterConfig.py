import logging
import configparser
import sys
import os
import threading
# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
BACKUP_XLSX_PATH = "backup_replacement_data.xlsx"
LANGUAGE_FOLDER = "languages"
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQKz1tiROR-S8zLK6YkrR5OPsvsuJAEVi1uC1ecTKk5-MLC-g6_jzIvSwAUNdnN5kyuIzbvU2DkmH1g/pub?output=xlsx"
DEFAULT_BEFORE_REPLACEMENT = ""
DEFAULT_AFTER_REPLACEMENT = " "
LINK_EDIT_FILE = "https://docs.google.com/spreadsheets/d/16uVFfVMKR7jVXA70g4BCo8KAE7iZVYnJT48oTpD1Z-4/edit?gid=0#gid=0"

# Global variables
last_mouse_position = (0, 0)
mouse_moved_significantly = False
is_paused = False
keyboard_thread_running = False
current_replacement_data = {}
stop_event = threading.Event()  # Global event to signal thread stop

# Load settings from .ini file
config = configparser.ConfigParser()
config.read('settings.ini')

# Load language settings
language_config = configparser.ConfigParser()

# Function to determine the base path (works in both script and frozen modes)
def get_base_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

# Determine the path to the languages folder
BASE_PATH = get_base_path()
LANGUAGES_FOLDER = os.path.join(BASE_PATH, "languages")

# Get settings or use defaults
SHEET_URL = config.get('Settings', 'sheet_url', fallback="https://docs.google.com/spreadsheets/d/e/2PACX-1vQKz1tiROR-S8zLK6YkrR5OPsvsuJAEVi1uC1ecTKk5-MLC-g6_jzIvSwAUNdnN5kyuIzbvU2DkmH1g/pub?output=xlsx") #DEFAULT_SHEET_URL
BEFORE_REPLACEMENT = config.get('Settings', 'before_replacement', fallback=DEFAULT_BEFORE_REPLACEMENT)
AFTER_REPLACEMENT = config.get('Settings', 'after_replacement', fallback=DEFAULT_AFTER_REPLACEMENT)

# Track previous values of the widgets
previous_sheet_url = SHEET_URL
previous_before_replacement = BEFORE_REPLACEMENT
previous_after_replacement = AFTER_REPLACEMENT
