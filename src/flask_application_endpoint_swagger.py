from automapping.m5_pipeline import M5
from automapping.language import Language
from automapping.preprocessor import Abbreviations, EntityExtractor
from automapping.translator import HuggingFace
from automapping.concept import Concept
from automapping.mapper import TfIdf
from automapping.detections import Predictions
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import pandas as pd
import yaml


app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="API for M5",
    description="German-English term translation & German-OMOP mapping within translation",
)

ns = api.namespace("API")

translate_model = api.model(
    "TranslateTable",
    {
        "host": fields.String(required=True, description="Host address"),
        "data_dictionary": fields.String(
            required=True, description="The name of the data dictionary"
        ),
        "version": fields.Integer(required=True, description="Version number"),
        "table": fields.String(required=True, description="Table name"),
    },
)


@ns.route("/translate_table")
class TranslateTable(Resource):
    """
    Endpoint to translate table with swagger documentation
    """

    @api.expect(translate_model)
    @api.response(200, "Success")
    def post(self):
        """
        Endpoint to translate table
        """
        host = request.form.get("host")
        data_dictionary = request.form.get("data_dictionary")
        version = request.form.get("version")
        table = request.form.get("table")

        configuration = M5(
            host, data_dictionary, version, table, Language.GERMAN, Language.ENGLISH
        )
        list_elements = [i for i, _ in configuration.loader()]
        list_variables = [j for _, j in configuration.loader()]
        model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
        translated_variables = model_translator.translate(
            list_variables,
            Abbreviations.load_abbreviations(
                config["abbreviations"]["file"],
                config["abbreviations"]["name_of_abbreviation_column"],
                config["abbreviations"]["name_of_description_column"],
            ),
        )
        configuration.translation_uploader(list_elements, list(translated_variables))

        return jsonify(
            {
                "status": "success",
                "message": "All translated variables have been uploaded.",
                "variables": list(translated_variables),
            }
        )


map_table_model = api.model(
    "MapTable",
    {
        "host": fields.String(required=True, description="Host address"),
        "data_dictionary": fields.String(
            required=True, description="The name of the data dictionary"
        ),
        "version": fields.Integer(required=True, description="Version number"),
        "table": fields.String(required=True, description="Table name"),
        "vocabulary_name": fields.String(
            required=True, description="Vocabulary name (SNOMED, LOINC)"
        ),
        "num_maps": fields.Integer(
            required=True, description="Number of maps to generate"
        ),
    },
)


@ns.route("/map_table")
class MapTable(Resource):
    """
    Endpoint to translate and map table
    """

    @api.expect(map_table_model)
    @api.response(200, "Success")
    def post(self):
        """
        Endpoint to map table
        """
        host = request.form.get("host")
        data_dictionary = request.form.get("data_dictionary")
        version = request.form.get("version")
        table = request.form.get("table")
        vocabulary_name = request.form.get("vocabulary_name")
        num_maps = request.form.get("num_maps")

        configuration = M5(
            host, data_dictionary, version, table, Language.GERMAN, Language.ENGLISH
        )
        list_elements = [i for i, _ in configuration.loader()]
        list_variables = [j for _, j in configuration.loader()]
        model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
        translated_variables = model_translator.translate(
            list_variables,
            Abbreviations.load_abbreviations(
                config["abbreviations"]["file"],
                config["abbreviations"]["name_of_abbreviation_column"],
                config["abbreviations"]["name_of_description_column"],
            ),
        )
        model_entity = EntityExtractor()
        preprocessed_data = list(model_entity(translated_variables))
        concepts = pd.read_csv(
            config["concepts"]["file"],
            on_bad_lines="skip",
            delimiter="\t",
            low_memory=False,
        )
        synonyms = pd.read_csv(
            config["synonyms"]["file"],
            on_bad_lines="skip",
            delimiter="\t",
            low_memory=False,
        )
        vocabulary_table = pd.read_csv(
            config["vocabulary_table"]["file"],
            on_bad_lines="skip",
            delimiter="\t",
            low_memory=False,
        )
        concepts = Concept.concatenate_concept_with_their_synonyms(
            concepts, synonyms, vocabulary_table, str(vocabulary_name)
        )
        model_map = TfIdf(concepts)
        mapping = model_map(preprocessed_data, list_elements)
        df_predictions = Predictions.to_df(mapping, int(num_maps))
        configuration.concept_uploader(df_predictions, str(vocabulary_name))
        return {
            "status": "success",
            "message": "The variables from the table has been successfully mapped.",
        }


if __name__ == "__main__":
    with open(
        "C://Users/admin/OneDrive/Desktop/work_project/de.uke.iam.automapping/src/config.yaml",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)
    app.run(debug=True)
