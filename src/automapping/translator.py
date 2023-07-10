from transformers import pipeline
from .sample import Sample
from .language import Language


class Translator:
    """
    Tranlation of the sample
    """

    def translate(self, sample: Sample) -> Sample:
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

    def translate(self, sample: Sample) -> Sample:
        translator = pipeline("translation", self.model)
        sample.content = translator(sample.content)[0].get("translation_text")
        sample.language = self.target_language
        return sample
