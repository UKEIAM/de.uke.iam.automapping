from dataclasses import dataclass, field

import pandas as pd

from .sample import Sample


@dataclass
class Predictions:
    """
    The results of the automapping.
    """

    _detections: Sample
    df_with_results: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.df_with_results = self._filtering_dublicates()

    def _filtering_dublicates(self):
        """
        Method to get unique ConceptID for each SourceName
        """
        # Creating list of dictionaries from _detections
        data_list = {
            "SourceID": self._detections.unique_id,
            "SourceName": self._detections.content,
            "concepts": [
                {
                    "targetConceptName": prediction.concept.name,
                    "targetConceptID": prediction.concept.concept_id,
                    "targetConceptCode": prediction.concept.concept_code,
                    "targetDomainID": prediction.concept.domain_id,
                    "targetVocabularyVersion": prediction.concept.voc_version,
                    "MatchScore": prediction.score,
                }
                for prediction in self._detections.concepts
            ],  # Converting each concept into dictionary
        }
        df_with_results = pd.DataFrame(data_list)
        # from concepts column create new dataframe using dictionary inside and then combine them
        df_with_results = pd.concat(
            [
                df_with_results.drop(["concepts"], axis=1),
                df_with_results["concepts"].apply(pd.Series),
            ],
            axis=1,
        )
        # find duplicate by targetConceptID and keep first
        df_with_results = df_with_results.drop_duplicates(
            subset=["SourceID", "targetConceptID"], keep="first"
        ).reset_index(drop=True)
        return df_with_results

    def to_df(self, num_guesses: int) -> pd.DataFrame:
        """
        Get a dataframe with the predictions.
        """
        df_with_final_results = (
            self.df_with_results.groupby(["SourceID", "SourceName"])
            .head(num_guesses)
            .reset_index(drop=True)
        )
        df_with_final_results = df_with_final_results.sort_values(
            "SourceName"
        ).reset_index(drop=True)
        df_with_final_results = (
            df_with_final_results.groupby(["SourceID", "SourceName"])
            .apply(lambda x: x.sort_values(["MatchScore"], ascending=False))
            .reset_index(drop=True)
        )
        return df_with_final_results
