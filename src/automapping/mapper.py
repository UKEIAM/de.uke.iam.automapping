from dataclasses import dataclass
from typing import Sequence
from numpy import matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from .concept import Concept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    source_names: str
    concept_ids: int
    concept_names: str
    confidence_scores: float


class Mapper:
    """
    The final step in the pipeline mapping text input to existing concepts.
    """

    def __call__(self, data: str, num_guesses: int) -> Sequence[Prediction]:
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

    def __call__(self, data: str, num_guesses: int) -> Sequence[Prediction]:
        matrix_with_similarity_score = (
            self.create_matrix_with_cosine_sim_between_term_concept(data)
        )
        source_names = []
        concept_ids = []
        concept_names = []
        confidence_score = []
        for i in range(matrix_with_similarity_score.shape[0]):
            for seq_number, score in heapq.nlargest(
                num_guesses,
                enumerate(matrix_with_similarity_score[i]),
                key=lambda x: x[1],
            ):
                source_names.append(data[i])
                concept_ids.append(self.concepts.concept_id[seq_number])
                concept_names.append(self.concepts.names[seq_number])
                confidence_score.append(score)
        return Prediction(
            source_names,
            concept_ids,
            concept_names,
            confidence_score,
        )

    def create_matrix_with_cosine_sim_between_term_concept(self, data: str) -> matrix:
        """
        Method for creating a matrix with cosine similarity between term and concept.
        """
        tfidf = TfidfVectorizer()
        concepts_tfidf = tfidf.fit_transform(self.concepts.names)
        source_tfidf = tfidf.transform(data)
        return cosine_similarity(source_tfidf, concepts_tfidf)
