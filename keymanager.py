#!filepath: keymanager.py
import logging
import os
from pathlib import Path

from pyupdater.key_handler.keys import KeyImporter, Keys
from pyupdater.utils.exceptions import KeyInvalidError

logger = logging.getLogger(__name__)

class KeyManager:
    """Manages the creation of new keypacks.

    Args:
        app_name (str): The name of the application.
    """

    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
        self.keypack_filename = f"{app_name}-keypack.pyu"

    def create_keypack(self, output_dir: str = ".") -> None:
        """Creates a new keypack and saves it to a file.

        Args:
            output_dir (str): The directory where the keypack file will be saved.

        Raises:
            FileExistsError: If a keypack file already exists.
            KeyInvalidError: If there is an error importing the keys.
            Exception: For other unexpected errors.
        """
        keypack_path = Path(output_dir) / self.keypack_filename
        if keypack_path.exists():
            raise FileExistsError(
                f"Keypack file already exists at: {keypack_path}"
            )

        try:
            keys = Keys(self.app_name)
            key_importer = KeyImporter(
                key_data=keys.get_public(),
                key_type="public",
                filename=str(keypack_path),
            )
            key_importer.start()
            logger.info(f"Keypack created successfully at: {keypack_path}")

        except KeyInvalidError as e:
            logger.error(f"Error importing keys: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app_name = "MyExampleApp"
    output_directory = "keypack"
    os.makedirs(output_directory, exist_ok=True)

    try:
        key_manager = KeyManager(app_name=app_name)
        key_manager.create_keypack(output_dir=output_directory)
    except (FileExistsError, KeyInvalidError, Exception) as e:
        logger.error(e)