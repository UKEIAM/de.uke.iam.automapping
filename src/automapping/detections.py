from .prediction import Prediction
import pandas as pd


class Predictions:
    """
    A view for the results of the automapping.
    """

    def __init__(self, generator):
        self.source_names = []
        self.concept_names = []
        self.concept_ids = []
        self.confidence_scores = []

        for item in generator:
            self.source_names.append(item.source_name)
            self.concept_names.append(item.concept_name)
            self.concept_ids.append(item.concept_id)
            self.confidence_scores.append(item.confidence_score)

    def __len__(self):
        return len(self.source_names)

    def __getitem__(self, key):
        return Prediction(
            source_name=self.source_names[key],
            concept_id=self.concept_ids[key],
            concept_name=self.concept_names[key],
            confidence_score=self.confidence_scores[key],
        ).__new__()

    def __setitem__(self, key: int, value: Prediction):
        self.source_names[key] = value.source_name
        self.concept_names[key] = value.concept_name
        self.concept_ids[key] = value.concept_id
        self.confidence_scores[key] = value.confidence_score

    def to_df(self) -> pd.DataFrame:
        """
        Get a dataframe with the predictions.
        """
        df_with_results = pd.DataFrame()
        df_with_results["SourceName"] = self.source_names
        df_with_results["ConceptName"] = self.concept_names
        df_with_results["ConceptID"] = self.concept_ids
        df_with_results["MatchScore"] = self.confidence_scores
        return df_with_results
