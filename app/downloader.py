# steeleye_assignment/downloader.py

import os
import logging
import requests
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Downloader:
    """
    Handles downloading of XML and ZIP files from given URLs.

    Attributes:
        download_dir (str): Path to the directory where files will be saved.
    """

    def __init__(self, download_dir: str = "downloads"):
        """
        Initializes the downloader and ensures the download directory exists.

        Args:
            download_dir (str): Directory where files will be downloaded.
        """
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        logger.info(f"Download directory set to: {self.download_dir}")

    def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """
        Downloads a file from the specified URL.

        Args:
            url (str): The URL to download the file from.
            filename (Optional[str]): Optional name to save the file as.

        Returns:
            str: Full path to the downloaded file.

        Raises:
            requests.exceptions.RequestException: If the download fails.
        """
        logger.info(f"Downloading file from URL: {url}")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise

        if not filename:
            filename = url.split("/")[-1]

        file_path = os.path.join(self.download_dir, filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"File saved to: {file_path}")
        return file_path
