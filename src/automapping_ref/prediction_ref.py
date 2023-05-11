from dataclasses import dataclass


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    concept: Concept
