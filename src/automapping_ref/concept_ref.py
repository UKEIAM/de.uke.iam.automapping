from dataclasses import dataclass


@dataclass
class OmopConcept:
    """
    A concept in a medical ontology from OMOP CDM.
    """

    name: str
    concept_id: int
    concept_code: int
    domain_id: str
    voc_version: str


class Concept(OmopConcept):
    """
    A concept in a medical ontology
    """

    name: str
    concept_id: int
    concept_code: int
    domain_id: str
    voc_version: str

    def get_name(self) -> str:
        return self.name
