import loader
import translator
import preprocessor
#from translator import HuggingFace
#from loader import ExcelLoader, Loader
#from preprocessor import EntityExtractor
#from preprocessor import Abbreviations
#from preprocessor import Preprocessor



model=translator.HuggingFace("en")
data=loader.ExcelLoader('/workspaces/de.uke.iam.automapping/experiments/VM_Soarian_HCHS_20210422.xlsx', 'Langname')#, 'de')
abbreviations=preprocessor.Abbreviations.list_of_abbreviations('/workspaces/de.uke.iam.automapping/experiments/german_abbreviation.xlsx', 'Abbreviation', 'Description')
#print(model.translate(data, Abbreviations(abbreviations)))
result_of_translation=model.translate(data, preprocessor.Abbreviations(abbreviations))
data_extraction=preprocessor.EntityExtractor()
a=data_extraction(result_of_translation)
print(list(a))


