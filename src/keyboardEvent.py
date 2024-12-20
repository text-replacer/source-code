# src/keyboardEvent.py
import keyboard
import logging, time
from pynput import mouse
from src.starterConfig import *
import pyperclip
import win32clipboard

def replace_word(word, replacement):
    """
    Replace the typed word or selected text with the replacement text.
    """
    logging.info(f"Replacing '{word}' with '{replacement}'")
    # Simulate pressing backspace to delete the typed word
    keyboard.write("\b" * (len(word) + 1))
    
    # Split the replacement text by newlines and simulate typing each part
    replacement_parts = replacement.split('\n')
    keyboard.write(BEFORE_REPLACEMENT)
    # for part in replacement_parts:
    #     keyboard.write(part)
    #     if part != replacement_parts[-1]:  # If not the last part, press Enter
    #         keyboard.press_and_release('enter')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(replacement, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    keyboard.press_and_release('ctrl+v')

    keyboard.write(AFTER_REPLACEMENT)
    
def on_mouse_move(x, y):
    """
    Callback function to detect significant mouse movement.
    This is used to reset the buffer of typed characters if the mouse moves significantly,
    preventing accidental replacements after the user has moved the cursor away.
    """
    global last_mouse_position, mouse_moved_significantly
    # Check if the mouse has moved more than 10 pixels in any direction
    if abs(x - last_mouse_position[0]) > 10 or abs(y - last_mouse_position[1]) > 10:
        mouse_moved_significantly = True
        last_mouse_position = (x, y)

# Start listening for mouse events
mouse_listener = mouse.Listener(on_move=on_mouse_move)
mouse_listener.start()

def on_key_event(replacement_data):
    """
    Callback function to handle key events and detect words between spaces.
    """
    # Buffer to store typed characters
    buffer = []
    # Create a set from replacement_data keys for faster lookups
    replacement_words = set(replacement_data.keys())

    def handle_key(event):
        nonlocal buffer
        global mouse_moved_significantly, is_paused

        if is_paused:
            return

        if event.event_type == keyboard.KEY_DOWN:
            # if mouse_moved_significantly:
            #     buffer = []
            #     mouse_moved_significantly = False

            if event.name in ['space', 'enter']:
                # Try to get currently selected text
                # Get current selection by simulating Ctrl+C
                current_selection = pyperclip.paste().strip()
                if current_selection:
                    # Selection is detected
                    if current_selection in replacement_words:
                        replace_word(current_selection, replacement_data[current_selection])
                        buffer = [] # Empty the buffer
                        pyperclip.copy('')  # Clear clipboard after replacement
                    else:
                        # Selection does not match a key in the dictionary
                        word = "".join(buffer)
                         # Use the set for fast lookup
                        if word in replacement_words:
                            replace_word(word, replacement_data[word])
                        buffer = []
                else:
                    if mouse_moved_significantly:
                        buffer = []
                        mouse_moved_significantly = False
                    word = "".join(buffer)
                    # Use the set for fast lookup
                    if word in replacement_words:
                        replace_word(word, replacement_data[word])
                    buffer = []
            elif event.name == 'backspace':
                if buffer:
                    buffer.pop()
            # Only allow alphanumeric and specific special characters
            elif event.name.isalnum() and event.name not in ['ctrl', 'enter', 'capslock', 'shift']:
                buffer.append(event.name)
    return handle_key

def start_keyboard_listener(replacement_data):
    """
    Starts the keyboard hook in a separate thread.
    """
    global keyboard_thread_running
    if keyboard_thread_running:
        stop_keyboard_hook()
    stop_event.clear()  # Clear the stop event before starting the thread
    keyboard_thread = threading.Thread(target=start_keyboard_hook, args=(replacement_data,))
    keyboard_thread.daemon = True  # Daemon thread will exit when the main program exits
    keyboard_thread.start()
    keyboard_thread_running = True  # Set the flag to indicate the thread is running
    logging.info("Listening for keyboard input...")

def start_keyboard_hook(replacement_data):
    """
    Start the keyboard hook in a separate thread.
    """
    global stop_event
    keyboard.hook(on_key_event(replacement_data))
    
    while not stop_event.is_set():  # Loop until the stop event is set
        time.sleep(TIME_INTERVAL_KEYBOARD_CHECK)  # Sleep for 100 milliseconds to reduce CPU usage
    
    # Clean up when the thread is stopped
    keyboard.unhook_all()
    logging.info("Keyboard hook stopped.")

def stop_keyboard_hook():
    """
    Signal the keyboard hook thread to stop.
    """
    global stop_event
    stop_event.set()  # Set the stop event to signal the thread to stop
    # logging.info("Stopping keyboard hook thread...")