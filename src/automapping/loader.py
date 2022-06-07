from typing import Iterable
import pandas as pd
import numpy as np
#import language


class Loader:
    """
    A class loading samples from a source.
    """

    def __init__(self):#, language: language.Language):
        pass
        #self.language = language

    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class ExcelLoader(Loader):
    """
    Load a column from a given Excel file.
    """

    def __init__(self, path: str, column: str):#, language: language.Language):
        #super().__init__(language)
        self.path=path
        self.column=column

    def __iter__(self) -> Iterable[str]:
        data=pd.read_excel(self.path, usecols=[self.column])
        data=data.replace([' ', ''], np.nan)
        data[self.column]=data[self.column].str.strip()
        data=data[self.column].dropna(axis=0)
        return iter(data)
