from dataclasses import dataclass
from typing import Sequence
from numpy import matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from concept import Concept


@dataclass
class Prediction:
    """
    A prediction with associated confidence score.
    """

    term: str
    predicted_id: int
    predicted_name: str
    confidence: float


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
        terms = []
        concept_ids = []
        concept_names = []
        sim_score = []
        for i in range(matrix_with_similarity_score.shape[0]):
            for seq_number, score in heapq.nlargest(
                num_guesses,
                enumerate(matrix_with_similarity_score[i]),
                key=lambda x: x[1],
            ):
                terms.append(data[i])
                concept_ids.append(self.concepts.concept_id[seq_number])
                concept_names.append(self.concepts.names[seq_number])
                sim_score.append(score)
        return Prediction(
            terms,
            concept_ids,
            concept_names,
            sim_score,
        )

    def create_matrix_with_cosine_sim_between_term_concept(self, data: str) -> matrix:
        """
        Make a correlation matrix between the two documents.
        """
        tfidf = TfidfVectorizer()
        concepts_tfidf = tfidf.fit_transform(self.concepts.names)
        terms_tfidf = tfidf.transform(data)
        return cosine_similarity(terms_tfidf, concepts_tfidf)
