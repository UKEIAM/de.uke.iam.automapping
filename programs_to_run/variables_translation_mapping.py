import sys

sys.path.insert(0, "/workspaces/de.uke.iam.automapping/src/automapping")

from language import Language
from loader import M5Loader
from translator import HuggingFace
from preprocessor import Abbreviations
from preprocessor import EntityExtractor
from concept import Concept
from mapper import TfIdf
from detections import Predictions
import pandas as pd
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Translate phrases from German to English inside M5"
    )
    parser.add_argument(
        "-d",
        "--data_dictionary",
        type=str,
        help="Data dictionary from M5, like HCHS",
        required=True,
    )
    parser.add_argument(
        "-v", "--version", type=int, help="Version of data dictionary", required=True
    )
    parser.add_argument(
        "-t", "--table", type=str, help="Name of the table", required=True
    )
    parser.add_argument(
        "-p",
        "--path_to_abbreviation",
        type=str,
        help="Path to the table with abbreviations and description",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--abbreviation_column",
        type=str,
        help="Name of the column with abbreviations",
        required=True,
    )
    parser.add_argument(
        "-de",
        "--description_column",
        type=str,
        help="Name of the column with descriptions",
        required=True,
    )
    parser.add_argument(
        "-p_concept",
        "--path_to_concept",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    parser.add_argument(
        "-p_synonym",
        "--path_to_concept_synonyms",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    parser.add_argument(
        "-voc",
        "--vocabulary_name",
        type=str,
        nargs="+",
        help="Vocabulary name(SNOMED..)",
        required=True,
    )

    parser.add_argument(
        "-n",
        "--number_matches",
        type=int,
        help="Number of matches",
        required=True,
    )

    args = parser.parse_args()
    model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
    translated_phrases = model_translator.translate(
        M5Loader(args.data_dictionary, args.version, args.table, Language.GERMAN),
        Abbreviations.load_abbreviations(
            args.path_to_abbreviation, args.abbreviation_column, args.description_column
        ),
    )
    model_entity = EntityExtractor()
    prep_data = model_entity(translated_phrases)
    synonyms = pd.read_csv(
        args.path_to_synonym, on_bad_lines="skip", delimiter="\t", low_memory=False
    )
    concepts = pd.read_csv(
        args.path_to_concept_synonyms,
        on_bad_lines="skip",
        delimiter="\t",
        low_memory=False,
    )
    concepts = Concept.concatenate_concept_with_their_synonyms(
        concepts, synonyms, [args.vocabulary_name]
    )
    model_mapping = TfIdf(concepts)

    get_the_pred = Predictions(model_mapping(prep_data))
    result = get_the_pred.to_df(args.number_matches)
    print(result)


if __name__ == "__main__":
    main()
