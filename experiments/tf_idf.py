from utils import make_dataframe
from utils import comparing_dataframes
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq



class Mapper:
    """
    Step of TF-IDF implementation
    """

    def __init__(self, num_guesses:int, data:list, dictionary: dict, concept_id_list: list, init_df):
        self.num_guesses=num_guesses
        self.data=data
        self.dictionary=dictionary
        self.concept_id_list=concept_id_list
        self.init_df=init_df
    
    def matrix_creation(self):
        """
        Make a correlation matrix between the two documents.
        """
        tfidf=TfidfVectorizer()
        vecs=tfidf.fit_transform(self.data)
        corr_matrix = ((vecs * vecs.T).A)
        return corr_matrix

    def similarity_matrix(self, matrix_correlation):
        """
        Cut only part of corr matrix where is similarity's score for every term with every concept.

        Variables
        -------
        matrix - correlation matrix between documents
        """
        length=len(self.dictionary['terms'])#TODO variable
        return matrix_correlation[:length , length:]


    def similar_concept(self, matrix_similarity):
        """
        Get TOP concept guesses. 

        Variables
        --------
        matrix - similarity matrix 
        """
        concepts_similarity={}
        for i in range(matrix_similarity.shape[0]):
            term=self.dictionary['terms'][i]#TODO variables
            concepts_similarity[term]=[]
            concepts_list=[self.dictionary['concepts'][a] for a in heapq.nlargest(self.num_guesses, range(len(matrix_similarity[i])), matrix_similarity[i].__getitem__)]
            sim_list=heapq.nlargest(self.num_guesses, matrix_similarity[i])
            concept_ids=[self.concept_id_list[a] for a in heapq.nlargest(self.num_guesses, range(len(matrix_similarity[i])), matrix_similarity[i].__getitem__)]
            concepts_similarity[term].append((concepts_list, concept_ids, sim_list))
        return concepts_similarity


    def map(self):
        """
        Method for getting dataframe with top similar concepts to terms
        """
        Correletaion_matrix=self.matrix_creation()
        Similarity_matrix=self.similarity_matrix(Correletaion_matrix)
        concept_dict=self.similar_concept(Similarity_matrix)
        df_new=make_dataframe(concept_dict, self.dictionary, self.init_df)

        return comparing_dataframes(self.init_df, df_new, self.num_guesses)

