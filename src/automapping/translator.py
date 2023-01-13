from abc import abstractmethod
from transformers import pipeline
from typing import Sequence
from .language import Language
from .preprocessor import Preprocessor


class Translator:
    """
    A step in the pipeline doing the actual translation.
    """

    @abstractmethod
    def translate(
        self, data: Sequence[str], preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        """
        Translation step
        """
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class HuggingFace(Translator):
    """
    Use HuggingFace for translations.
    """

    def __init__(self, source_language: Language, target_language: Language):
        self.target_language = target_language
        self.source_language = source_language
        self.model = f"Helsinki-NLP/opus-mt-{self.source_language.value}-{self.target_language.value}"

    def translate(
        self, data: Sequence[str], preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        tr_list = []
        translator = pipeline("translation", self.model)
        samples = list(preprocessor(data))
        for sample in translator(samples):
            tr_list.append(sample.get("translation_text"))
        return tr_list
