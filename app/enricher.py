# steeleye_assignment/enricher.py

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataEnricher:
    """
    Adds enrichment columns to the DLTINS DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df (pd.DataFrame): DataFrame to enrich.
        """
        self.df = df

    def enrich(self) -> pd.DataFrame:
        """
        Adds two columns:
        - 'a_count': number of lowercase 'a' in FullNm
        - 'contains_a': 'YES' if a_count > 0, else 'NO'

        Returns:
            pd.DataFrame: Enriched DataFrame
        """
        logger.info("Adding enrichment columns (a_count and contains_a)")

        self.df["a_count"] = self.df["FinInstrmGnlAttrbts.FullNm"].apply(
            lambda x: x.count("a") if isinstance(x, str) else 0
        )

        self.df["contains_a"] = self.df["a_count"].apply(
            lambda x: "YES" if x > 0 else "NO"
        )

        logger.info("Enrichment completed.")
        return self.df
