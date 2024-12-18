from re import I
import logging
import atexit

from src.starterConfig import *
from src.languages import *
from src.processXlsx import *
from src.keyboardEvent import *
from src.tkGUI import *
import win32clipboard
import time
from threading import Thread

def start_program():
    """
    Restart the program by reloading all settings and replacement data.
    """
    replacement_data = load_settings_and_data()
    if replacement_data:
        start_keyboard_listener(replacement_data)
        clipboard_thread = Thread(target=monitor_clipboard, args=(replacement_data,), daemon=True)
        clipboard_thread.start()
        logging.info("Clipboard monitoring started.")
    else:
        logging.error("Failed to start program. Exiting program.")


def monitor_clipboard(replacement_data):
    while True:
        try:
            win32clipboard.OpenClipboard()
            content = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).strip().lower()
            win32clipboard.CloseClipboard()
            # logging.info(f"Clipboard content: {content}")
            keys_of_replacement_data = list(replacement_data.keys())
            # logging.info(f"Clipboard content: {keys_of_replacement_data}")
            # logging.info(f"Clipboard content: {content in keys_of_replacement_data}")
            if content in keys_of_replacement_data:
                new_content = replacement_data[content]
                logging.info(f"Clipboard content: {new_content}")
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(new_content, win32clipboard.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                keyboard.press_and_release('ctrl+v')
        except TypeError:
            # Handle the case where clipboard content is not text
            pass
        except Exception as e:
            logging.error(f"Error accessing clipboard: {e}")
        
        time.sleep(TIME_INTERVAL_CLIPBOARD_CHECK)  # Check clipboard once per second to reduce CPU usage

start_program()

atexit.register(stop_keyboard_hook)
# Run the GUI
root.mainloop()
