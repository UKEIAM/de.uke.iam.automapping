from dataclasses import dataclass
import pandas as pd

# from typing import Iterable, Sequence


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    def __init__(self, path: str, vocabulary_id: str, standart_concept: str):
        self.path = path
        self.vocabulary_id = vocabulary_id
        self.standart_concept = standart_concept
        self.omop_concepts = pd.read_csv(
            path, on_bad_lines="skip", delimiter="\t", low_memory=False
        )

    def __call__(self):
        concepts = self.omop_concepts[
            (self.omop_concepts["vocabulary_id"] == self.vocabulary_id)
            & (self.omop_concepts["standard_concept"] == self.standart_concept)
        ]
        # concepts = concepts[['concept_id', 'concept_name']]
        concepts_id = concepts["concept_id"].tolist()
        concept_names = list(map(str, concepts["concept_name"]))
        return concepts_id, concept_names
