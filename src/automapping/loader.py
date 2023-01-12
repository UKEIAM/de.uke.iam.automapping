from typing import Tuple

import numpy as np
import pandas as pd

from .language import Language


class Loader:
    """
    A class loading samples from a source.
    """

    def __init__(self, language: Language):
        self.language = language

    def __call__(self) -> Tuple["pd.Series[str]", "pd.Series[str]"]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class ExcelLoader(Loader):
    """
    Load variables with their identifiers from a given Excel file.

    return: identifiers, variables
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

    def __call__(self) -> Tuple["pd.Series[str]", "pd.Series[str]"]:
        self.data = self.data.replace([" ", ""], np.nan)
        self.data[self.column_variable] = self.data[self.column_variable].str.strip()
        identifiers = self.data[self.column_ident].dropna(axis=0)
        variables = self.data[self.column_variable].dropna(axis=0)
        return identifiers, variables
