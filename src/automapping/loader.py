from typing import Iterable

import numpy as np
import pandas as pd

from .language import Language


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

    def __init__(
        self, path: str, column_ident: str, column_variable: str, language: Language
    ):
        super().__init__(language)
        self.path = path
        self.column_ident = column_ident
        self.column_variable = column_variable
        self.data = pd.read_excel(
            self.path, usecols=[self.column_ident, self.column_variable]
        )

    def __iter__(self) -> Iterable[tuple]:
        self.data = self.data.replace([" ", ""], np.nan)
        self.data[self.column_variable] = self.data[self.column_variable].str.strip()
        self.data = self.data.apply(tuple, axis=1)
        return iter(self.data)
