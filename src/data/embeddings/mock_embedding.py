""" A mocking embedding for testing purposes. """

from . import Embedding, WordVectors, Sample, Language


class MockEmbedding(Embedding):
    """
    A mock embedding used for testing purposes.
    """

    def supports_language(self, _: Language) -> bool:
        """
        Checks whether the object supports a language.
        """
        return True

    def transform(self, sample: Sample) -> WordVectors:
        """
        Tranform a sample in a supported language into word vectors.
        """
        return WordVectors.from_iterable(
            sample.language, ([i] for i, _ in enumerate(sample.phrase.split()))
        )
