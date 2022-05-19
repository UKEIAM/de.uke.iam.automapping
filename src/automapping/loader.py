from typing import Iterable

from . import Language


class Loader:
    """
    A class loading samples from a source.
    """

    def __init__(self, language: Language):
        self.language = language

    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class ExcelLoader(Loader):
    """
    Load a column from a given Excel file.
    """

    def __init__(self, path: str, column: str, language: Language):
        super().__init__(language)
        raise NotImplementedError()

    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError()
