from typing import Iterable

import requests

from .language import Language


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

    def loader(self, language: Language) -> Iterable[str]:
        """
        Load data from M5
        """
        data_json = requests.Session().get(url=self.url).json()
        for element in data_json["elements"]:
            for label in element["labels"]:
                if label["language"] == language.value.upper():
                    yield element["name"], label["value"]

    def translation_uploader(
        self, names_of_elements: list, translated_values: list, language: Language
    ):
        """
        Upload translated data to M5
        """
        header = {"Content-type": "application/json", "Accept": "application/json"}
        for i, element in enumerate(names_of_elements):
            body = requests.get(self.url + "/" + element, timeout=10).json()
            if language.value.upper() not in body["definitions"].keys():
                body["labels"].append(
                    {
                        "language": language.value.upper(),
                        "value": translated_values[i],
                        "type": "PREFERED",
                    }
                )
                body["definitions"]["EN"] = translated_values[i]
            upd = requests.patch(
                self.url + "/" + element, json=body, headers=header, timeout=10
            )
            print(upd)