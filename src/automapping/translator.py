from transformers import pipeline
from typing import Sequence 
from . import Loader
from . import Language
from . import Preprocessor


class Translator:
    """
    A step in the pipeline doing the actual translation.
    """

    def __init__(self, source_language: Language, target_language: Language):
        self.target_language = target_language
        self.source_language = source_language

    def translate(
        self, data: Loader, preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class HuggingFace(Translator):
    """
    Use HiggingFace for translations.

    """

    def __init__(self, source_language: Language, target_language: Language):
        self.target_language = target_language
        self.source_language = source_language
        self.model = f"Helsinki-NLP/opus-mt-{self.target_language.value}-{self.source_language.value}"

    def translate(
        self, data: Loader, preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        tr_list = []
        translator = pipeline("translation", self.model)
        samples = list(preprocessor(data))
        for sample in translator(samples):
            tr_list.append(sample.get("translation_text"))
        return tr_list
