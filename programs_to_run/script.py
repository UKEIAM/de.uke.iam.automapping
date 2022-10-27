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
    parser = argparse.ArgumentParser(description = 'Pipeline for translation or semantic mapping for m5 entities')
    subparser = parser.add_subparsers(dest="command")
    translating = subparser.add_parser("translating")
    mapping = subparser.add_parser("mapping")
    full_pipeline = subparser.add_parser("full_pipeline")

    #####################################
    # TODO: choose language for translation
    translating.add_argument(
        "-d",
        "--data_dictionary",
        type=str,
        help="Data dictionary from M5, like HCHS",
        required=True,
    )
    translating.add_argument(
        "-v", "--version", type=int, help="Version of data dictionary", required=True
    )
    translating.add_argument(
        "-t", "--table", type=str, help="Name of the table", required=True
    )
    translating.add_argument(
        "-p",
        "--path_to_abbreviation",
        type=str,
        help="Path to the table with abbreviations and description",
        required=True,
    )
    translating.add_argument(
        "-a",
        "--abbreviation_column",
        type=str,
        help="Name of the column with abbreviations",
        required=True,
    )

    translating.add_argument(
        "-de",
        "--description_column",
        type=str,
        help="Name of the column with descriptions",
        required=True,
    )

    ########################################################

    mapping.add_argument(
        "-d",
        "--data_dictionary",
        type=str,
        help="Data dictionary from M5, like HCHS",
        required=True,
    )
    mapping.add_argument(
        "-v", "--version", type=int, help="Version of data dictionary", required=True
    )
    mapping.add_argument(
        "-t", "--table", type=str, help="Name of the table", required=True
    )

    mapping.add_argument(
        "-p_concept",
        "--path_to_concept",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    mapping.add_argument(
        "-p_synonym",
        "--path_to_concept_synonyms",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    mapping.add_argument(
        "-voc",
        "--vocabulary_name",
        nargs="+",
        type=str,
        help="Vocabulary name(SNOMED..)",
        required=True,
    )

    mapping.add_argument(
        "-n",
        "--number_matches",
        type=int,
        help="Number of matches",
        required=True,
    )

    ############################################################

    full_pipeline.add_argument(
        "-d",
        "--data_dictionary",
        type=str,
        help="Data dictionary from M5, like HCHS",
        required=True,
    )
    full_pipeline.add_argument(
        "-v", "--version", type=int, help="Version of data dictionary", required=True
    )
    full_pipeline.add_argument(
        "-t", "--table", type=str, help="Name of the table", required=True
    )
    full_pipeline.add_argument(
        "-p",
        "--path_to_abbreviation",
        type=str,
        help="Path to the table with abbreviations and description",
        required=True,
    )
    full_pipeline.add_argument(
        "-a",
        "--abbreviation_column",
        type=str,
        help="Name of the column with abbreviations",
        required=True,
    )

    full_pipeline.add_argument(
        "-de",
        "--description_column",
        type=str,
        help="Name of the column with descriptions",
        required=True,
    )
    full_pipeline.add_argument(
        "-p_concept",
        "--path_to_concept",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    full_pipeline.add_argument(
        "-p_synonym",
        "--path_to_concept_synonyms",
        type=str,
        help="Path to the table with concepts",
        required=True,
    )
    full_pipeline.add_argument(
        "-voc",
        "--vocabulary_name",
        nargs="+",
        type=str,
        help="Vocabulary name(SNOMED..)",
        required=True,
    )

    full_pipeline.add_argument(
        "-n",
        "--number_matches",
        type=int,
        help="Number of matches",
        required=True,
    )

    #####################################################

    args = parser.parse_args()

    if args.command == "translating":
        translated_data = translation_pipeline(
            loading_data(args.data_dictionary, args.version, args.table),
            args.path_to_abbreviation,
            args.abbreviation_column,
            args.description_column,
        )
        print(list(translated_data))

    elif args.command == "mapping":
        df_with_mapped_data = mapping_pipeline(
            loading_data(args.data_dictionary, args.version, args.table),
            args.path_to_concept,
            args.path_to_concept_synonyms,
            args.vocabulary_name,
            args.number_matches,
        )
        print(df_with_mapped_data)

    elif args.command == "full_pipeline":
        translated_data = translation_pipeline(
            loading_data(args.data_dictionary, args.version, args.table),
            args.path_to_abbreviation,
            args.abbreviation_column,
            args.description_column,
        )
        df_with_mapped_data = mapping_pipeline(
            translated_data,
            args.path_to_concept,
            args.path_to_concept_synonyms,
            args.vocabulary_name,
            args.number_matches,
        )
        print(df_with_mapped_data)


def loading_data(data_dictionary, version_of_data_dictionary, name_of_the_table):
    data = M5Loader(
        data_dictionary,
        version_of_data_dictionary,
        name_of_the_table,
        Language.GERMAN,
    )
    return data


def translation_pipeline(
    data,
    path_to_abbreviation_list,
    name_of_abbreviation_column,
    name_of_description_column,
):
    model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
    translated_phrases = model_translator.translate(
        data,
        Abbreviations.load_abbreviations(
            path_to_abbreviation_list,
            name_of_abbreviation_column,
            name_of_description_column,
        ),
    )
    return translated_phrases


def mapping_pipeline(
    data, path_to_concept, path_to_concept_synonyms, vocabulary_name, number_matches
):
    model_entity = EntityExtractor()
    prep_data = list(model_entity(data))
    concepts = pd.read_csv(
        path_to_concept, on_bad_lines="skip", delimiter="\t", low_memory=False
    )
    synonyms = pd.read_csv(
        path_to_concept_synonyms,
        on_bad_lines="skip",
        delimiter="\t",
        low_memory=False,
    )
    concepts = Concept.concatenate_concept_with_their_synonyms(
        concepts, synonyms, vocabulary_name
    )
    model_mapping = TfIdf(concepts)
    get_the_pred = Predictions(model_mapping(prep_data))
    result = get_the_pred.to_df(number_matches)
    return result


if __name__ == "__main__":
    main()
