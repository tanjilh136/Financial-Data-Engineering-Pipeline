# steeleye_assignment/csv_writer.py

import os
import logging
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


class CSVWriter:
    """
    Writes a pandas DataFrame to a CSV file.
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory set to: {self.output_dir}")

    def save_to_csv(self, df: pd.DataFrame, filename: str = "dltins_output.csv") -> Optional[str]:
        """
        Saves the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            filename (str): Name of the output file.

        Returns:
            Optional[str]: The path to the saved file or None on failure.
        """
        output_path = os.path.join(self.output_dir, filename)

        try:
            df.to_csv(output_path, index=False)
            logger.info(f"CSV saved successfully at: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to write CSV: {e}")
            return None
