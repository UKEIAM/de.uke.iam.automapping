import heapq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .sample import Sample
from .prediction import Prediction
from .concepts import OmopConcepts


class Mapper:
    """
    The final step in the pipeline mapping text input to existing concepts.
    """

    def __call__(self, sample: Sample) -> Prediction:
        """
        Map a given input to the top guesses sorted in descending order.
        """

        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class TfIdf(Mapper):
    """
    A mapper using Tf-Idf for mapping.
    """

    def __init__(self, concepts: OmopConcepts):
        self.concepts = concepts
        self.tfidf = TfidfVectorizer()
        self.concepts_tfidf = self.tfidf.fit_transform(concepts.get_names())

    def __call__(self, sample: Sample) -> Sample:
        sample_tfidf = self.tfidf.transform([sample.content])
        matrix_with_similarity_score = cosine_similarity(
            sample_tfidf, self.concepts_tfidf
        )
        predictions_list = []
        for seq_number, score in heapq.nlargest(
            100,
            enumerate(matrix_with_similarity_score[0]),
            key=lambda x: x[1],
        ):
            predictions_list.append(Prediction(self.concepts[seq_number], score))
        return Sample(
            sample.unique_id, sample.content, sample.language, predictions_list
        )
