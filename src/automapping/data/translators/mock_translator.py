""" A mock translator doing nothing. """

from typing import Tuple

from . import Translator, Language, SequenceVector


class MockTranslator(Translator):
    """
    A mock translator doing nothing.
    """

    def __init__(self, language: Language) -> None:
        self.language = language

    def supported_languages(self) -> Tuple[Language, Language]:
        return (self.language, self.language)

    def translate(self, vector: SequenceVector) -> SequenceVector:
        return vector
