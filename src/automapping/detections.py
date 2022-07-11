from dataclasses import dataclass
from .prediction import Prediction
from typing import Sequence
import pandas as pd


@dataclass
class Predictions:
    """
    A view for the results of the automapping.
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
        df_with_results = pd.DataFrame()
        df_with_results["SourceName"] = list(
            map(lambda x: x.source_name, self._detections)
        )
        df_with_results["ConceptName"] = list(
            map(lambda x: x.concept_name, self._detections)
        )
        df_with_results["ConceptID"] = list(
            map(lambda x: x.concept_id, self._detections)
        )
        df_with_results["MatchScore"] = list(
            map(lambda x: x.confidence_score, self._detections)
        )
        return df_with_results
