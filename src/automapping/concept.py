from dataclasses import dataclass
from typing import Sequence

import pandas as pd


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    concept_id: int
    names: Sequence[str]
    domain_ids: Sequence[str]

    @staticmethod
    def concatenate_concept_with_their_synonyms(
        path_concepts: str, path_synonyms: str, vocabulary_id: str
    ) -> "Concept":
        """
        Method for concatenation concepts and their synonyms
        """

        concepts = pd.read_csv(
            path_concepts, on_bad_lines="skip", delimiter="\t", low_memory=False
        )
        concepts = concepts[
            (concepts["vocabulary_id"] == vocabulary_id)
            & (concepts["standard_concept"] == "S")
        ]
        concepts["concept_name"] = (
            concepts["concept_name"].replace({"X]": "X] "}, regex=True).str.lower()
        )
        main_concept_ids = concepts["concept_id"].tolist()
        main_domain_ids = concepts["domain_id"].tolist()
        main_concept_names = list(map(str, concepts["concept_name"]))
        synonyms = pd.read_csv(
            path_synonyms, on_bad_lines="skip", delimiter="\t", low_memory=False
        )
        synonyms = synonyms[synonyms["concept_id"].isin(main_concept_ids)]
        synonyms_concept_ids = synonyms["concept_id"].tolist()
        synonyms_domain_ids = ["Synonym"] * synonyms.shape[0]
        synonyms_concept_names = list(
            map(str, synonyms["concept_synonym_name"].str.lower())
        )
        return Concept(
            main_concept_ids + synonyms_concept_ids,
            main_concept_names + synonyms_concept_names,
            main_domain_ids + synonyms_domain_ids,
        )
