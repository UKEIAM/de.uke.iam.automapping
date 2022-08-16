from dataclasses import dataclass
from typing import Sequence

import pandas as pd


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    names: Sequence[str]
    concept_id: int
    domain_ids: Sequence[str]

    @staticmethod
    def concatenate_concept_with_their_synonyms(
        concepts: pd.DataFrame, synonyms: pd.DataFrame, vocabulary_ids: Sequence[str]
    ) -> "Concept":
        """
        Method for concatenation concepts and their synonyms
        """
        concepts = concepts[
            (concepts["vocabulary_id"].isin(vocabulary_ids))
            & (concepts["standard_concept"] == "S")
        ]
        concepts["concept_name"] = (
            concepts["concept_name"].replace({"X]": "X] "}, regex=True).str.lower()
        )
        main_concept_ids = concepts["concept_id"].tolist()
        main_domain_ids = concepts["domain_id"].tolist()
        main_concept_names = list(map(str, concepts["concept_name"]))
        synonyms = synonyms[synonyms["concept_id"].isin(main_concept_ids)]
        synonyms_concept_ids = synonyms["concept_id"].tolist()
        synonyms_domain_ids = ["Synonym"] * synonyms.shape[0]
        synonyms_concept_names = list(
            map(str, synonyms["concept_synonym_name"].str.lower())
        )
        return Concept(
            main_concept_names + synonyms_concept_names,
            main_concept_ids + synonyms_concept_ids,
            main_domain_ids + synonyms_domain_ids,
        )
