from automapping.m5_pipeline import M5
from automapping.language import Language
from automapping.preprocessor import Abbreviations
from automapping.translator import HuggingFace
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/translate_table", methods=["POST"])
def translate_table():
    """
    Endpoint to translate table
    """
    host = request.form.get("host")
    data_dictionary = request.form.get("data_dictionary")
    version = request.form.get("version")
    table = request.form.get("table")
    # source_language = request.form.get('source_language')
    # target_language = request.form.get('target_language')

    configuration = M5(
        host, data_dictionary, version, table, Language.GERMAN, Language.ENGLISH
    )
    list_elements = [i for i,_ in configuration.loader()]
    list_variables = [j for _,j in configuration.loader()]
    model_translator = HuggingFace(Language.GERMAN, Language.ENGLISH)
    translated_variables = model_translator.translate(
        list_variables,
        Abbreviations.load_abbreviations(
            "C://Users/admin/OneDrive/Desktop/work_project/de.uke.iam.automapping/src/automapping/german_abbreviation.xlsx",
            "Abbreviation",
            "Description",
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
