from automapping.m5_pipeline import M5
from automapping.language import Language
from automapping.preprocessor import Abbreviations
from automapping.translator import HuggingFace
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import yaml


app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Translate Table API",
    description="A simple translation API",
)

ns = api.namespace("api", description="Translation operations")

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
        with open("C://Users/admin/OneDrive/Desktop/work_project/de.uke.iam.automapping/src/config.yaml", encoding="utf-8") as file:
            config = yaml.safe_load(file)

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


if __name__ == "__main__":
    app.run(debug=True)
