from dataclasses import dataclass
from typing import Sequence

import pandas as pd


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    names: Sequence[str]
    concept_id: Sequence[int]
    concept_code: Sequence[int]
    domain_ids: Sequence[str]
    voc_version: Sequence[str]

    @staticmethod
    def concatenate_concept_with_their_synonyms(
        concepts: pd.DataFrame,
        synonyms: pd.DataFrame,
        vocabulary_table: pd.DataFrame,
        vocabulary_id: str,
    ) -> "Concept":
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
        main_concept_ids = concepts["concept_id"].tolist()
        main_concept_codes = concepts["concept_code"].tolist()
        main_domain_ids = concepts["domain_id"].tolist()
        main_concept_names = list(map(str, concepts["concept_name"]))
        synonyms = synonyms[synonyms["concept_id"].isin(main_concept_ids)]
        synonyms = synonyms.merge(concepts, on="concept_id", how="left")
        synonyms_concept_ids = synonyms["concept_id"].tolist()
        synonyms_concept_codes = synonyms["concept_code"].tolist()
        synonyms_domain_ids = ["Synonym"] * synonyms.shape[0]
        synonyms_concept_names = list(
            map(str, synonyms["concept_synonym_name"].str.lower())
        )
        voc_version = vocabulary_table[
            vocabulary_table["vocabulary_id"] == vocabulary_id
        ].iloc[0]["vocabulary_version"]
        voc_version_list = [voc_version] * len(
            main_concept_names + synonyms_concept_names
        )
        return Concept(
            main_concept_names + synonyms_concept_names,
            main_concept_ids + synonyms_concept_ids,
            main_concept_codes + synonyms_concept_codes,
            main_domain_ids + synonyms_domain_ids,
            voc_version_list,
        )
