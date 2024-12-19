# src/updater.py
from pyupdater.client import Client
import logging
import os
import platform
from src.starterConfig import *
from src.client_config import ClientConfig  # Create & use client_config.py

# Setup logging for updater
log = logging.getLogger('pyupdater')
log.setLevel(logging.DEBUG)
log_file_handler = logging.FileHandler('update.log')
log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(log_file_handler)

VERSION_FILE = 'version.txt'
PLATFORM = 'win' if platform.system() == 'Windows' else 'linux' if platform.system() == 'Linux' else 'mac'

# Define the path to the app
BASE_PATH = get_base_path()

# Get the path to the update folder
UPDATE_PATH = os.path.join(BASE_PATH, 'updates')

def get_current_version():
   version_file_path = os.path.join(BASE_PATH, VERSION_FILE)
   try:
       if os.path.exists(version_file_path):
           with open(version_file_path, 'r') as f:
               return f.read().strip()
       else:
           return "0.0.1"
   except Exception as e:
       log.error(f"Error reading version file: {e}")
       return "0.0.1"
  
def update_version(version):
   version_file_path = os.path.join(BASE_PATH, VERSION_FILE)
   try:
       with open(version_file_path, 'w') as f:
           f.write(str(version))
           log.info(f"Updated version file to version: {version}")
   except Exception as e:
       log.error(f"Error writing version file: {e}")

def print_status_info(info):
    total = info.get(u'total')
    downloaded = info.get(u'downloaded')
    status = info.get(u'status')
    log.info(f"{status}: {downloaded} of {total}")

def check_for_new_update():
   client = Client(ClientConfig(), refresh=True, progress_hooks=[print_status_info])

   app_update = client.update_check(ClientConfig.APP_NAME, get_current_version())
   if app_update:
       log.info("Update available, downloading...")
       app_update.download()
       if app_update.is_downloaded():
           log.info("Update downloaded successfully.")
           log.info("Extracting and restarting...")
           update_version(app_update.version) # Update version before restarting
           app_update.extract_restart()
       else:
           log.error("Update download failed.")
   else:
       log.info("No updates available.")