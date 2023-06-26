from dataclasses import dataclass
from .concept import OmopConcept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    concept: OmopConcept
    score: float
