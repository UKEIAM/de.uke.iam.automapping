from dataclasses import dataclass
from typing import Sequence


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    concept_id: int
    names: Sequence[str]
    domain_ids: Sequence[str]
