from .mapper import Prediction
from typing import Sequence
import pandas as pd


class View:
    """
    A view for the results of the automapping.
    """

    @staticmethod
    def to_df(predictions: Sequence[Prediction]) -> pd.DataFrame:
        """
        Get a dataframe with the predictions.
        """
        df_with_results = pd.DataFrame()
        df_with_results["SourceName"] = predictions.source_names
        df_with_results["ConceptName"] = predictions.concept_names
        df_with_results["ConceptID"] = predictions.concept_ids
        df_with_results["MatchScore"] = predictions.confidence_scores
        return df_with_results
