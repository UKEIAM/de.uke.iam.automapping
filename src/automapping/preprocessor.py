from typing import Iterable, Mapping
import re
import pandas as pd
import spacy



class Preprocessor:
    """
    A step in the pipeline preprocessing the raw input.
    """

    def __call__(self, data: Iterable[str]) -> Iterable[str]:#подставить результаты из loader 

        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )



class Abbreviations(Preprocessor):
    """
    A step in the pipeline removing abbreviations given a mapping.
    """

    def __init__(self, mapping: Mapping[str, str]):
        # You can add a static method for reading the mapping from e.g. a Excel file.
        self.mapping = mapping


    @staticmethod
    def list_of_abbreviations(path, name_of_abbreviation_column, name_of_description_column):
        """
        Reading the mapping from Excel file with abbreviations.
        """
        df=pd.read_excel(path)
        df=df[[name_of_abbreviation_column, name_of_description_column]]
        return df


    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        for sample in data:
            for raw_tuple in self.mapping.itertuples():
                sample = re.sub(r'\b' + raw_tuple[1] + r'[^\w]', raw_tuple[2] + ' ', sample)
            yield sample



class EntityExtractor(Preprocessor):
    """
    A step in the pipeline removing uneccessary word.
    """
    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        ready_list=[]
        nlp=spacy.load('en_core_web_lg')
        nlp.Defaults.stop_words.remove('no')
        nlp.Defaults.stop_words.remove('not')
        nlp.Defaults.stop_words.remove('none')
        nlp.Defaults.stop_words.remove('noone')
        nlp.Defaults.stop_words.remove('back')
        nlp.Defaults.stop_words.add('doctor')
        for sample in data:
            sample=sample.lower()
            token_list=[]
            doc=nlp(sample)
            token_list=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
            text = " ".join(token_list)
            ready_list.append(text)
        return iter(ready_list)




            # Do something with sample here
            #raise NotImplementedError()
            #yield sample


#x=Abbreviations(mapping data)
#x(loader)
#abb=Abbreviations.list_of_abbreviations('/workspaces/de.uke.iam.automapping/experiments/german_abbreviation.xlsx', 'Abbreviation', 'Description')
#print(abb)
#a=Abbreviations(abb)
#print(a(ExcelLoader('/workspaces/de.uke.iam.automapping/experiments/VM_Soarian_HCHS_20210422.xlsx', 'Langname', 'de')))
#a=Abbreviations(mapping=abb)
#print(list(a(ExcelLoader('/workspaces/de.uke.iam.automapping/experiments/VM_Soarian_HCHS_20210422.xlsx', 'Langname', 'de'))))

#print(list(ExcelLoader('/workspaces/de.uke.iam.automapping/experiments/VM_Soarian_HCHS_20210422.xlsx', 'Langname', 'de')


