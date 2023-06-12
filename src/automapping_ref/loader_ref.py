from sample_ref import Sample
from m5_ref import M5
from language_ref import Language
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
        self.data = self.data.head(10)
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

    def __init__(
        self,
        host: str,
        data_dictionary: str,
        version: int,
        table: str,
    ):
        self.host = host
        self.data_dictionary = data_dictionary
        self.version = version
        self.table = table
        self.url = f"http://{self.host}/m5.rest/api/{self.data_dictionary}/{self.version}/{self.table}"

    def load(self, source_language: Language) -> List[Sample]:
        m5 = M5(self.host, self.data_dictionary, self.version, self.table)
        return [
            Sample(name, value, source_language)
            for name, value in m5.loader(source_language)
        ]
