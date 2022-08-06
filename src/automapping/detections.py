from dataclasses import dataclass, field
from typing import Sequence

import pandas as pd

from .prediction import Prediction


@dataclass
class Predictions:
    """
    The results of the automapping.
    """

    _detections: Sequence[Prediction]
    df_with_results: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.df_with_results = self._filtering_dublicates()

    def __len__(self):
        return len(self._detections)

    def __getitem__(self, key):
        return self._detections[key]

    def __setitem__(self, key: int, value: Prediction):
        self._detections[key] = value

    def _filtering_dublicates(self):
        """
        Method to get unique ConceptID for each SourceName
        """
        df_with_results = pd.DataFrame.from_dict(list(self._detections))
        df_with_results.columns = [
            "SourceName",
            "ConceptID",
            "ConceptName",
            "DomainID",
            "MatchScore",
        ]
        df_with_results = df_with_results.drop_duplicates(
            subset=["SourceName", "ConceptID"], keep="first"
        ).reset_index(drop=True)
        return df_with_results

    def to_df(self, num_guesses: int) -> pd.DataFrame:
        """
        Get a dataframe with the predictions.
        """
        df_with_final_results = (
            self.df_with_results.groupby("SourceName")
            .head(num_guesses)
            .reset_index(drop=True)
        )
        return df_with_final_results
