from .sample import Sample
from .m5 import M5
from .language import Language
import pandas as pd
import numpy as np

from typing import List


class Loader:
    """
    A class loading samples from a source.
    """

    def load(self, source_language: Language) -> List[Sample]:
        """
        Function to load data from a source
        """
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class ExcelLoader(Loader):
    """
    Load samples from a given Excel file.
    """

    def __init__(self, path: str, column_ident: str, column_variable: str):
        self.path = path
        self.column_ident = column_ident
        self.column_variable = column_variable
        self.data = pd.read_excel(
            self.path, usecols=[self.column_ident, self.column_variable]
        )

    def load(self, source_language: Language) -> List[Sample]:
        self.data = pd.read_excel(
            self.path, usecols=[self.column_ident, self.column_variable]
        )
        self.data.replace([" ", ""], np.nan, inplace=True)
        self.data[self.column_variable] = self.data[self.column_variable].str.strip()
        self.data.dropna(axis=0, inplace=True)
        return [
            Sample(row[self.column_ident], row[self.column_variable], source_language)
            for _, row in self.data.iterrows()
        ]


class M5loader(Loader):
    """
    Load samples from M5
    """

    def __init__(self, m5_data: M5.loader):
        self.m5_data = m5_data

    def load(self, source_language: Language) -> List[Sample]:
        return [Sample(name, value, source_language) for name, value in self.m5_data]
