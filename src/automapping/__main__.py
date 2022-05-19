from data.sample import Sample
from data.language import Language

from data.embeddings.mock_embedding import MockEmbedding
from data.combinators.mock_combinator import MockCombinator
from data.translators.mock_translator import MockTranslator

if __name__ == "__main__":
    sample = Sample("This is a test", Language.ENGLISH)
    vectors = MockEmbedding().transform(sample)
    vector = MockCombinator().transform(vectors)
    translated_vector = MockTranslator(Language.ENGLISH).translate(vector)
