from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    name: str
    concept_id: int
    concept_code: int
    domain_id: str
    voc_version: str
    concept_synonyms: str

    @staticmethod
    def concatenate_concept_with_their_synonyms(
        concepts: pd.DataFrame,
        synonyms: pd.DataFrame,
        vocabulary_table: pd.DataFrame,
        vocabulary_id: str,
    ) -> Iterable["Concept"]:
        """
        Method for concatenation concepts and their synonyms
        """
        concepts = concepts[
            (concepts["vocabulary_id"] == vocabulary_id)
            & (concepts["standard_concept"] == "S")
        ]
        concepts["concept_name"] = (
            concepts["concept_name"].replace({"X]": "X] "}, regex=True).str.lower()
        )
        voc_version = vocabulary_table[
            vocabulary_table["vocabulary_id"] == vocabulary_id
        ].iloc[0]["vocabulary_version"]
        for _, concept in concepts.iterrows():
            concept_name = concept["concept_name"]
            concept_id = concept["concept_id"]
            concept_domain = concept["domain_id"]
            concept_code = concept["concept_code"]
            concept_synonyms = " ".join(
                synonyms[synonyms["concept_id"] == concept_id][
                    "concept_synonym_name"
                ].tolist()
            )
            yield Concept(
                concept_name,
                concept_id,
                concept_code,
                concept_domain,
                voc_version,
                concept_synonyms,
            )
