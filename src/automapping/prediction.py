from dataclasses import dataclass
from .concept import Concept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    concept: Concept
    score: float
