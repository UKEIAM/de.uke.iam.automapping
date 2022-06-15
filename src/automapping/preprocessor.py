from typing import Iterable, Mapping
import re
import pandas as pd
import spacy


class Preprocessor:
    """
    A step in the pipeline preprocessing the raw input.
    """

    def __call__(self, data: Iterable[str]) -> Iterable[str]:

        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class Abbreviations(Preprocessor):
    """
    A step in the pipeline removing abbreviations given a mapping.
    """

    def __init__(self, mapping: Mapping[str, str]):
        self.mapping = mapping

    @staticmethod
    def load_list_of_abbreviations(
        path: str, name_of_abbreviation_column: str, name_of_description_column: str
    ):
        """
        Reading the mapping from Excel file with abbreviations.
        """
        abbreviations = pd.read_excel(path)
        return abbreviations[[name_of_abbreviation_column, name_of_description_column]]

    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        for sample in data:
            for _, original, replacement in self.mapping.itertuples():
                sample = re.sub(r"\b" + original + r"[^\w]", replacement + " ", sample)
            yield sample


class EntityExtractor(Preprocessor):
    """
    A step in the pipeline removing uneccessary word.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.Defaults.stop_words.remove("no")
        self.nlp.Defaults.stop_words.remove("not")
        self.nlp.Defaults.stop_words.remove("none")
        self.nlp.Defaults.stop_words.remove("noone")
        self.nlp.Defaults.stop_words.remove("back")
        self.nlp.Defaults.stop_words.add("doctor")

    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        ready_list = []
        for sample in data:
            sample = sample.lower()
            token_list = []
            doc = self.nlp(sample)
            token_list = [
                token.lemma_
                for token in doc
                if not token.is_stop and not token.is_punct
            ]
            text = " ".join(token_list)
            ready_list.append(text)
        return iter(ready_list)
