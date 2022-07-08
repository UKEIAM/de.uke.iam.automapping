from dataclasses import dataclass


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    source_name: str
    concept_id: int
    concept_name: str
    confidence_score: float
