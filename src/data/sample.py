from dataclasses import dataclass

from .language import Language


@dataclass
class Sample:
    """
    A single sample with an associated language.
    """

    phrase: str
    language: Language

    def __str__(self) -> str:
        return f"'{self.phrase}' ({self.language})"
