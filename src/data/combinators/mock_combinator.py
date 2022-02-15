""" A mocking combinator for testing purposes. """

from . import Combinator, SequenceVector, WordVectors, Language


class MockCombinator(Combinator):
    """
    A mock combinator used for testing purposes.
    """

    def supports_language(self, _: Language) -> bool:
        """
        Checks whether the object supports a specific language.
        """
        return True

    def transform(self, words: WordVectors) -> SequenceVector:
        """
        Transform multiple supported word vectors into a single sequence vector.
        """
        return SequenceVector(
            vector=words.vectors.mean(axis=0), language=words.language
        )
