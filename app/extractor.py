# steeleye_assignment/extractor.py

import logging
import os
import zipfile
from typing import Optional

logger = logging.getLogger(__name__)


class Extractor:
    """
    Extracts files from ZIP archives and returns the path to the first XML file found.
    """

    def __init__(self, extract_dir: str = "extracted"):
        """
        Args:
            extract_dir (str): Directory where ZIP contents will be extracted.
        """
        self.extract_dir = extract_dir
        os.makedirs(self.extract_dir, exist_ok=True)
        logger.info(f"Extraction directory set to: {self.extract_dir}")

    def extract_xml(self, zip_path: str) -> Optional[str]:
        """
        Extracts the first XML file from the ZIP archive.

        Args:
            zip_path (str): Path to the ZIP file.

        Returns:
            Optional[str]: Path to the extracted XML file, or None if not found.
        """
        logger.info(f"Extracting ZIP file: {zip_path}")

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_dir)
                for name in zip_ref.namelist():
                    if name.endswith(".xml"):
                        xml_path = os.path.join(self.extract_dir, name)
                        logger.info(f"Extracted XML file: {xml_path}")
                        return xml_path

            logger.warning("No XML file found in ZIP.")
            return None

        except zipfile.BadZipFile as e:
            logger.error(f"Invalid ZIP file: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during extraction: {e}")
            return None
