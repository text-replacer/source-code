#!filepath: src/updater.py
# changed src/updater.py: Removed version file dependency, get version from client_config, open update URL instead of specific file.

import requests
import tkinter as tk
from packaging import version
from src.starterConfig import get_base_path
from src.client_config import ClientConfig

# Define the path to the app
BASE_PATH = get_base_path()

def get_current_version() -> str:
    """Retrieves the current version of the application from ClientConfig.

    Returns:
        str: The current version.
    """
    return ClientConfig.VERSION

def check_for_new_update(update_label, download_button) -> None:
    """Checks for updates and updates the GUI elements accordingly.

    Args:
        update_label (tk.Label): The label to display update status.
        download_button (tk.Button): The button to open the download page.
    """
    current_version = get_current_version()
    update_label.config(text=f"Current version: {current_version}")

    for update_url in ClientConfig.UPDATE_URLS:
        try:
            version_url = f"{update_url}/version.txt"
            response = requests.get(version_url, timeout=ClientConfig.HTTP_TIMEOUT)
            response.raise_for_status()
            latest_version = response.text.strip()

            if version.parse(latest_version) > version.parse(current_version):
                update_label.config(text=f"New version available: {latest_version}")
                download_button.config(
                    command=lambda: open_download_page(update_url),
                    state=tk.NORMAL,
                )
                download_button.config(state=tk.NORMAL)
                return
            else:
                update_label.config(text="You are on lastest version.")
                download_button.grid_forget()
                return

        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass

def open_download_page(update_url: str) -> None:
    """Opens the download page in the default web browser.

    Args:
        update_url (str): The base URL for updates.
    """
    import webbrowser
    webbrowser.open_new_tab(update_url)