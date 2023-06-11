from dataclasses import dataclass
from concept_ref import Concept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    concept: Concept
    score: float
