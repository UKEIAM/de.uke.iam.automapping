from typing import Sequence

from . import Language
from .loader import Loader
from .preprocessor import Preprocessor


class Translator:
    """
    A step in the pipeline doing the actual translation.
    """

    def __init__(self, target_language: Language):
        self.target_language = target_language

    def translate(
        self, data: Loader, preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class HuggingFace(Translator):
    """
    Use HiggingFace for translations.
    """

    def translate(
        self, data: Loader, preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        raise NotImplementedError()
