from dataclasses import dataclass


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    source_name: str
    concept_name: str
    concept_id: int
    domain_id: str
    confidence_score: float
