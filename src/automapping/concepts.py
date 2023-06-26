from dataclasses import dataclass
from typing import List
from .concept import OmopConcept, Concept

import pandas as pd


@dataclass
class Concepts:
    """
    Collection of concepts
    """

    concepts: List[Concept]


class OmopConcepts(Concepts):
    """
    Collection of concepts in a medical ontology like SNOMED-CT.
    """

    concepts: List[OmopConcept]

    def __getitem__(self, index):
        return self.concepts[index]

    def get_names(self):
        """
        Get names of the concepts
        """
        return [concept.get_name() for concept in self.concepts]

    @staticmethod
    def concatenate_concept_with_their_synonyms(
        concepts: pd.DataFrame,
        synonyms: pd.DataFrame,
        vocabulary_table: pd.DataFrame,
        vocabulary_id: str,
    ) -> "OmopConcepts":
        """
        Method for concatenation concepts and synonyms
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
        concepts_list = []
        for i, name in enumerate(main_concept_names):
            concepts_list.append(
                OmopConcept(
                    name,
                    main_concept_ids[i],
                    main_concept_codes[i],
                    main_domain_ids[i],
                    voc_version_list[i],
                )
            )

        for i, name in enumerate(synonyms_concept_names):
            concepts_list.append(
                OmopConcept(
                    name,
                    synonyms_concept_ids[i],
                    synonyms_concept_codes[i],
                    synonyms_domain_ids[i],
                    voc_version_list[i],
                )
            )
        return OmopConcepts(concepts_list)
