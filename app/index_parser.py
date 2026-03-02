# steeleye_assignment/index_parser.py

import logging
import xml.etree.ElementTree as ET
from typing import Optional

logger = logging.getLogger(__name__)


class IndexParser:
    """
    Parses an index XML file (non-namespaced) and extracts the second DLTINS download link.
    """

    def __init__(self, xml_path: str):
        self.xml_path = xml_path

    def get_second_dltins_url(self) -> Optional[str]:
        """
        Parses the XML and finds the second DLTINS download link.

        Returns:
            Optional[str]: The second DLTINS URL if found, else None.
        """
        logger.info(f"Parsing index XML: {self.xml_path}")

        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
        except Exception as e:
            logger.error(f"Failed to parse XML file: {e}")
            return None

        dltins_links = []

        for doc in root.findall(".//doc"):
            file_type = None
            download_link = None

            for field in doc.findall("str"):
                if field.attrib.get("name") == "file_type" and field.text == "DLTINS":
                    file_type = field.text
                if field.attrib.get("name") == "download_link":
                    download_link = field.text

            if file_type == "DLTINS" and download_link:
                dltins_links.append(download_link)

        if len(dltins_links) >= 2:
            logger.info(f"Found second DLTINS link: {dltins_links[1]}")
            return dltins_links[1]

        logger.warning("Second DLTINS link not found.")
        return None