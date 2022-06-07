from dataclasses import dataclass
#from typing import Sequence
#from typing import Iterable 
#TODO change types


@dataclass
class Concept:
    """
    A concept in a medical ontology like SNOMED-CT.
    """

    #concept_id: int
    #names: Sequence[str]
        
    def __init__(self, vocabulary_name, data):#, language: language.Language):
        #super().__init__(language)
        #self.path=path
        self.vocabulary_name=vocabulary_name #TODO to upcase
        self.data=data
        

    def get_concept(self):
        #TODO comments
        data_local=self.data[(self.data['vocabulary_id']==self.vocabulary_name) & (self.data['standard_concept']=='S')]
        data_local['concept_name']=data_local['concept_name'].replace({'X]': 'X] '}, regex=True)#TODO add exception
        data_local=data_local[['concept_name','concept_id']]
        return data_local

