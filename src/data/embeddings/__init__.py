"""
A module containing available embeddings to translate sentences into word vectors.
"""

from typing import Iterable, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np

from ..sample import Sample
from ..language import Language


@dataclass
class WordVectors:
    """
    A sequence of word vectors for a specific language.
    """

    vectors: np.ndarray
    language: Language

    def __post_init__(self):
        if len(self.vectors.shape) != 2:
            raise ValueError(
                "'vectors' must be a (n, d) array with n vectors and an embedding size of d"
            )

    def __len__(self) -> int:
        return len(self.vectors)

    def dim(self) -> int:
        """
        Calculate the dimension of the word vectors.
        """
        return self.vectors.shape[1]

    @classmethod
    def from_iterable(
        cls, language: Language, word_vectors: Iterable[List[float]]
    ) -> "WordVectors":
        """
        Create an object from an iterable (with at least one element) of word vectors.
        """

        word_vectors = list(word_vectors)
        data = np.zeros((len(word_vectors), len(word_vectors[0])), dtype=np.float32)
        for i, vector in enumerate(word_vectors):
            data[i, :] = vector
        return WordVectors(vectors=data, language=language)


class Embedding(ABC):
    """
    An embedding translating sentences into word vectors.
    """

    @abstractmethod
    def supports_language(self, _: Language) -> bool:
        """
        Checks whether the object supports a language.
        """
        raise NotImplementedError()

    @abstractmethod
    def transform(self, _: Sample) -> WordVectors:
        """
        Tranform a sample in a supported language into word vectors.
        """
        raise NotImplementedError()
