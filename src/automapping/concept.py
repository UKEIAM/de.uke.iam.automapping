from dataclasses import dataclass


@dataclass
class Concept:
    """
    A concept in a medical ontology
    """

    name: str
    concept_id: int
    concept_code: int
    domain_id: str
    voc_version: str


class OmopConcept(Concept):
    """
    A concept in a medical ontology from OMOP CDM.
    """

    name: str
    concept_id: int
    concept_code: int
    domain_id: str
    voc_version: str

    def get_name(self) -> str:
        """Get name of the concept"""
        return self.name
