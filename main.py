from re import I
import logging
import atexit

from src.starterConfig import *
from src.languages import *
from src.processXlsx import *
from src.keyboardEvent import *
from src.tkGUI import *

def start_program():
    """
    Restart the program by reloading all settings and replacement data.
    """
    replacement_data = load_settings_and_data()
    if replacement_data:
        start_keyboard_listener(replacement_data)
    else:
        logging.error("Failed to start program. Exiting program.")

start_program()

atexit.register(stop_keyboard_hook)
# Run the GUI
root.mainloop()
