from typing import Sequence
#from . import Language
from loader import Loader
#from language import Language
from preprocessor import Preprocessor
from transformers import pipeline
from loader import ExcelLoader
from preprocessor import Abbreviations


class Translator:
    """
    A step in the pipeline doing the actual translation.
    """

    def __init__(self):#, target_language: Language):
        #self.target_language = target_language
        pass

    def translate(
        self, data: Loader, preprocessor: Sequence[Preprocessor]
    ) -> Sequence[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class HuggingFace(Translator):
    """
    Use HiggingFace for translations.
    """

    def translate(self, data: Loader, preprocessor: Sequence[Preprocessor]) -> Sequence[str]:
        tr_list=[]
        model="Helsinki-NLP/opus-mt-de-en" #TODO using language class 
        translator=pipeline('translation', model)
        samples=list(preprocessor(data))
        for sample in translator(samples):
            tr_list.append(sample.get('translation_text'))
        return tr_list



#model=HuggingFace("en")
#data=ExcelLoader('/workspaces/de.uke.iam.automapping/experiments/VM_Soarian_HCHS_20210422.xlsx', 'Langname', 'de')
#abbreviations=Abbreviations.list_of_abbreviations('/workspaces/de.uke.iam.automapping/experiments/german_abbreviation.xlsx', 'Abbreviation', 'Description')
#print(model.translate(data, Abbreviations(abbreviations)))

#print(list(HuggingFace()))