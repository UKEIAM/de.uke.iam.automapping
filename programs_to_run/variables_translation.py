from language import Language
from loader import M5Loader
from translator import HuggingFace
from preprocessor import Abbreviations
import argparse


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
    args = parser.parse_args()
    model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
    translated_phrases = model_translator.translate(
        M5Loader(args.data_dictionary, args.version, args.table, Language.GERMAN),
        Abbreviations.load_abbreviations(
            args.path_to_abbreviation, args.abbreviation_column, args.description_column
        ),
    )
    print(list(translated_phrases))


if __name__ == "__main__":
    main()
