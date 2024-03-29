from .language import Language
from typing import Iterable
import requests
import logging
import pandas as pd


class M5:
    """
    Class contains functions to work with M5
    """

    def __init__(self, host: str, data_dictionary: str, version: int, table: str):
        self.host = host
        self.data_dictionary = data_dictionary
        self.version = version
        self.table = table
        self.url = f"http://{self.host}/m5.rest/api/{self.data_dictionary}/{self.version}/{self.table}"

    def loader(self, source_language: Language) -> Iterable[str]:
        """
        Load data from M5
        """
        data_json = requests.Session().get(url=self.url).json()
        for element in data_json["elements"]:
            for label in element["labels"]:
                if label["language"] == source_language.value.upper():
                    yield element["name"], label["value"]

    def translation_uploader(
        self,
        names_of_elements: list,
        translated_values: list,
        target_language: Language,
    ):
        """
        Upload translated data to M5
        """
        logging.basicConfig(level=logging.INFO)
        header = {"Content-type": "application/json", "Accept": "application/json"}
        for i, element in enumerate(names_of_elements):
            full_url = "/".join((self.url, element))
            body = requests.get(full_url, timeout=10).json()
            if target_language.value.upper() not in body["definitions"].keys():
                body["labels"].append(
                    {
                        "language": target_language.value.upper(),
                        "value": translated_values[i],
                        "type": "PREFERED",
                    }
                )
                body["definitions"][target_language.value.upper()] = translated_values[
                    i
                ]
            upd = requests.patch(full_url, json=body, headers=header, timeout=10)
            if upd.status_code == 200:
                logging.info("%s updated", element)

    def concept_uploader(self, result_table: pd.DataFrame, vocabulary_id: str):
        """
        Upload mapped concepts to M5
        """
        logging.basicConfig(level=logging.INFO)
        header = {"Content-type": "application/json", "Accept": "application/json"}
        for element in result_table["SourceID"].unique():
            full_url = "/".join((self.url, element))
            body = requests.get(full_url, timeout=10).json()
            body["concepts"] = []
            for _, data in result_table[result_table["SourceID"] == element].iterrows():
                body["concepts"].append(
                    {
                        "conceptType": vocabulary_id,
                        "conceptCode": data["targetConceptCode"],
                        "conceptVersion": data["targetVocabularyVersion"],
                        "conceptScore": data["MatchScore"],
                        "verified": "false",
                    }
                )
            upd = requests.patch(full_url, json=body, headers=header, timeout=10)
            if upd.status_code == 200:
                logging.info("%s updated", element)
