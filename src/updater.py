#!filepath: src/updater.py
import os
import platform
import requests
import tkinter as tk
from packaging import version
from src.starterConfig import get_base_path
from src.client_config import ClientConfig

VERSION_FILE = "version.txt"
PLATFORM = (
    "win"
    if platform.system() == "Windows"
    else "linux"
    if platform.system() == "Linux"
    else "mac"
)

# Define the path to the app
BASE_PATH = get_base_path()

def get_current_version() -> str:
    """Retrieves the current version of the application from the version file.

    Returns:
        str: The current version, or "0.0.1" if the version file does not exist or an error occurs.
    """
    version_file_path = os.path.join(BASE_PATH, VERSION_FILE)
    try:
        if os.path.exists(version_file_path):
            with open(version_file_path, "r") as f:
                return f.read().strip()
        else:
            return "0.0.1"
    except Exception:
        return "0.0.1"

def check_for_new_update(update_label: tk.Label, download_button: tk.Button) -> None:
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
                    command=lambda: open_download_page(update_url, latest_version),
                    state=tk.NORMAL,
                )
                # download_button.pack()
                download_button.config(state=tk.NORMAL)
                return
            else:
                update_label.config(text="No updates available.")
                return

        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass

def open_download_page(update_url: str, latest_version: str) -> None:
    """Opens the download page in the default web browser.

    Args:
        update_url (str): The base URL for updates.
        latest_version (str): The latest version available for download.
    """
    download_url = f"{update_url}/{ClientConfig.APP_NAME}-{latest_version}-{PLATFORM}.exe"
    import webbrowser

    webbrowser.open_new_tab(download_url)