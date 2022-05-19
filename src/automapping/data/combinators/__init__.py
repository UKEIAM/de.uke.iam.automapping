"""
The package containing the supported combinators.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np

from ..language import Language
from ..embeddings import WordVectors


@dataclass
class SequenceVector:
    """
    A single vector modelling a sequence of word vectors in a specific language.
    """

    vector: np.ndarray
    language: Language

    def __post_init__(self) -> None:
        if len(self.vector.shape) != 1:
            raise ValueError(
                "'vector' must be a (d,) numpy array with an embedding size of d"
            )


class Combinator(ABC):
    """
    A combinator combining multiple word vectors into a single sequence vector.
    """

    @abstractmethod
    def supports_language(self, _: Language) -> bool:
        """
        Checks whether the object supports a specific language.
        """
        raise NotImplementedError()

    @abstractmethod
    def transform(self, _: WordVectors) -> SequenceVector:
        """
        Transform multiple supported word vectors into a single sequence vector.
        """
        raise NotImplementedError()
