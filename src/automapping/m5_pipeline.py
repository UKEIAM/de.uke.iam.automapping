from typing import Iterable

import requests
import logging
import pandas as pd

from .language import Language


class M5:
    """
    Class contains functions to work with M5
    """

    def __init__(
        self,
        host: str,
        data_dictionary: str,
        version: int,
        table: str,
        source_language: Language,
        target_language: Language,
    ):
        self.source_language = source_language
        self.target_language = target_language
        self.host = host
        self.data_dictionary = data_dictionary
        self.version = version
        self.table = table
        self.url = f"http://{self.host}/m5.rest/api/{self.data_dictionary}/{self.version}/{self.table}"

    def loader(self) -> Iterable[str]:
        """
        Load data from M5
        """
        data_json = requests.Session().get(url=self.url).json()
        for element in data_json["elements"]:
            for label in element["labels"]:
                if label["language"] == self.source_language.value.upper():
                    yield element["name"], label["value"]

    def translation_uploader(self, names_of_elements: list, translated_values: list):
        """
        Upload translated data to M5
        """
        logging.basicConfig(level=logging.INFO)
        header = {"Content-type": "application/json", "Accept": "application/json"}
        for i, element in enumerate(names_of_elements):
            full_url = "/".join((self.url, element))
            body = requests.get(full_url, timeout=10).json()
            if self.target_language.value.upper() not in body["definitions"].keys():
                body["labels"].append(
                    {
                        "language": self.target_language.value.upper(),
                        "value": translated_values[i],
                        "type": "PREFERED",
                    }
                )
                body["definitions"][
                    self.target_language.value.upper()
                ] = translated_values[i]
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
                        "conceptCode": data["targetConceptID"],  # make it concept_code
                        "conceptVersion": data["targetVocabularyVersion"],
                        "conceptScore": data["MatchScore"],
                        "verified": "false",
                    }
                )
            upd = requests.patch(full_url, json=body, headers=header, timeout=10)
            if upd.status_code == 200:
                logging.info("%s updated", element)
