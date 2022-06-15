from typing import Iterable
import pandas as pd
import numpy as np
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
        self.path = path
        self.column = column
        self.data = pd.read_excel(self.path, usecols=[self.column])

    def __iter__(self) -> Iterable[str]:
        self.data = self.data.replace([" ", ""], np.nan)
        self.data[self.column] = self.data[self.column].str.strip()
        self.data = self.data[self.column].dropna(axis=0)
        return iter(self.data)
