# steeleye_assignment/dltins_parser.py

import logging
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Optional

logger = logging.getLogger(__name__)


class DLTINSParser:
    """
    Parses the extracted DLTINS XML and converts it to a pandas DataFrame.
    """

    def __init__(self, xml_path: str):
        """
        Args:
            xml_path (str): Path to the extracted DLTINS XML file.
        """
        self.xml_path = xml_path

    def parse_to_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Extracts FinInstrmGnlAttrbts and Issr fields into a DataFrame.

        Returns:
            Optional[pd.DataFrame]: The parsed data, or None on failure.
        """
        logger.info(f"Parsing DLTINS XML: {self.xml_path}")

        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
        except Exception as e:
            logger.error(f"Failed to parse XML: {e}")
            return None

        records = []

        for instrm in root.findall(".//{*}FinInstrm"):
            try:
                gnl = instrm.find(".//{*}FinInstrmGnlAttrbts")
                record = {
                    "FinInstrmGnlAttrbts.Id": gnl.find(".//{*}Id").text if gnl is not None else None,
                    "FinInstrmGnlAttrbts.FullNm": gnl.find(".//{*}FullNm").text if gnl is not None else None,
                    "FinInstrmGnlAttrbts.ClssfctnTp": gnl.find(".//{*}ClssfctnTp").text if gnl is not None else None,
                    "FinInstrmGnlAttrbts.CmmdtyDerivInd": gnl.find(".//{*}CmmdtyDerivInd").text if gnl is not None else None,
                    "FinInstrmGnlAttrbts.NtnlCcy": gnl.find(".//{*}NtnlCcy").text if gnl is not None else None,
                    "Issr": instrm.find(".//{*}Issr").text,
                }
                records.append(record)
            except Exception as e:
                logger.warning(f"Skipping malformed record: {e}")
                continue

        if not records:
            logger.warning("No valid records found.")
            return None

        df = pd.DataFrame(records)
        logger.info(f"Parsed {len(df)} records.")
        return df
