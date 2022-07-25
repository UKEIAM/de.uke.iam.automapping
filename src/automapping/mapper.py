from typing import Sequence
from numpy import matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from .concept import Concept
from .detections import Predictions
from .prediction import Prediction


class Mapper:
    """
    The final step in the pipeline mapping text input to existing concepts.
    """

    def __call__(self, data: str, num_guesses: int) -> Predictions:
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

    def __init__(self, concepts: Sequence[Concept]):
        self.concepts = concepts
        self.tfidf = TfidfVectorizer()
        self.concepts_tfidf = self.tfidf.fit_transform(self.concepts.names)

    def __call__(self, data: str, num_guesses: int) -> Predictions:
        matrix_with_similarity_score = (
            self._create_matrix_with_cosine_sim_between_term_concept(data)
        )
        predictions_list = []
        for i in range(matrix_with_similarity_score.shape[0]):
            for seq_number, score in heapq.nlargest(
                num_guesses,
                enumerate(matrix_with_similarity_score[i]),
                key=lambda x: x[1],
            ):
                predictions_list.append(
                    Prediction(
                        data[i],
                        self.concepts.concept_id[seq_number],
                        self.concepts.names[seq_number],
                        self.concepts.domain_id[seq_number],
                        score,
                    )
                )
        return Predictions(predictions_list)

    def _create_matrix_with_cosine_sim_between_term_concept(self, data: str) -> matrix:
        """
        Method for creating a matrix with cosine similarity between term and concept.
        """
        source_tfidf = self.tfidf.transform(data)
        return cosine_similarity(source_tfidf, self.concepts_tfidf)
