from dataclasses import dataclass
from .prediction import Prediction
from typing import Sequence
import pandas as pd


@dataclass
class Predictions:
    """
    The results of the automapping.
    """

    _detections: Sequence[Prediction]

    def __len__(self):
        return len(self._detections)

    def __getitem__(self, key):
        return self._detections[key]

    def __setitem__(self, key: int, value: Prediction):
        self._detections[key] = value

    def to_df(self) -> pd.DataFrame:
        """
        Get a dataframe with the predictions.
        """
        df_with_results = pd.DataFrame.from_dict(list(self._detections))
        df_with_results.columns = [
            "SourceName",
            "ConceptID",
            "ConceptName",
            "DomainID",
            "MatchScore",
        ]
        return df_with_results
