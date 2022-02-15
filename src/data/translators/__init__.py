"""
The package containing the supported translators.
"""

from abc import ABC, abstractmethod
from typing import Tuple

from ..language import Language
from ..combinators import SequenceVector


class Translator(ABC):
    """
    A translator used to transform a sequence vector in one language into another.
    """

    @abstractmethod
    def supported_languages(self) -> Tuple[Language, Language]:
        """
        Returns the language mapping.
        """
        raise NotImplementedError()

    @abstractmethod
    def translate(self, _: SequenceVector) -> SequenceVector:
        """
        Transform a sequence vector in one language into another
        """
        raise NotImplementedError()
