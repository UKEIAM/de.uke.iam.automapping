import spacy
from .sample import Sample
from typing import Sequence, Mapping
from nltk.stem import PorterStemmer
import pandas as pd
import re


class Preprocessor:
    """
    Preprocessing of the sample
    """

    def transform(self, sample: Sample) -> Sample:
        """
        Preprocessing step
        """
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class AbbreviationReplacement(Preprocessor):
    """
    A step in the pipeline removing abbreviations given a mapping.
    """

    def __init__(self, mapping: Mapping[str, str]):
        self.mapping = mapping

    @staticmethod
    def load_abbreviations(
        path: str, name_of_abbreviation_column: str, name_of_description_column: str
    ) -> Preprocessor:
        """
        Reading the mapping from Excel file with abbreviations.
        """
        abbreviations = pd.read_excel(path)
        return AbbreviationReplacement(
            abbreviations[[name_of_abbreviation_column, name_of_description_column]]
        )

    def transform(self, sample: Sample) -> Sample:
        for _, original, replacement in self.mapping.itertuples():
            sample.content = re.sub(
                r"\b" + original + r"[^\w]", replacement + " ", sample.content
            )
        return sample


class SpacyPreprocessor(Preprocessor):
    """
    Use Spacy for preprocessing of the sample with custumized spacy pipeline.
    """

    def __init__(
        self,
        pipeline: Sequence[str] = [
            "lowercase",
            "stopwords",
            "lemmatizer",
            "punctuation",
        ],
    ):
        self.pipeline = pipeline
        self.nlp = spacy.load("en_core_web_sm")
        self.stemmer = PorterStemmer()
        self.nlp.Defaults.stop_words.remove("no")
        self.nlp.Defaults.stop_words.remove("not")
        self.nlp.Defaults.stop_words.remove("none")
        self.nlp.Defaults.stop_words.remove("noone")
        self.nlp.Defaults.stop_words.remove("back")
        self.nlp.Defaults.stop_words.add("doctor")

    def transform(self, sample: Sample) -> Sample:
        doc = self.nlp(sample.content)
        if "lowercase" in self.pipeline:
            sample.content = " ".join([token.text.lower() for token in doc])
            doc = self.nlp(sample.content)
        if "stopwords" in self.pipeline:
            sample.content = " ".join(
                [token.text for token in doc if not token.is_stop]
            )
            doc = self.nlp(sample.content)
        if "lemmatizer" in self.pipeline:
            sample.content = " ".join([token.lemma_ for token in doc])
            doc = self.nlp(sample.content)
        if "punctuation" in self.pipeline:
            sample.content = " ".join(
                [token.text for token in doc if not token.is_punct]
            )
            doc = self.nlp(sample.content)
        if "stemmer" in self.pipeline:
            sample.content = " ".join([self.stemmer.stem(token.text) for token in doc])
            doc = self.nlp(sample.content)
        return sample