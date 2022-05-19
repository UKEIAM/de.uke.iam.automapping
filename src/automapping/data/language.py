"""
A module containing language identifiers.
"""

from enum import Enum


class Language(Enum):
    """
    A supported language by the mapping tool.
    """

    ENGLISH = "en"
    GERMAN = "de"

    def __str__(self) -> str:
        return self.value
