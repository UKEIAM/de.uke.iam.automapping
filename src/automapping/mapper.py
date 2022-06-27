from dataclasses import dataclass
from typing import Sequence

from .concept import Concept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    predicted_id: int
    confidence: float


class Mapper:
    """
    The final step in the pipeline mapping text input to existing concepts.
    """

    def __call__(self, data: str, num_guesses: int) -> Sequence[Prediction]:
        """
        Map a given input to the top guesses sorted in descending order.
        """

        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class TfIdf(Mapper):
    """
    A mapper using Tf-Idf for mapping.
    """

    def __init__(self, concepts: Sequence[Concept]):
        raise NotImplementedError()

    def __call__(self, data: str, num_guesses: int) -> Sequence[Prediction]:
        raise NotImplementedError()
