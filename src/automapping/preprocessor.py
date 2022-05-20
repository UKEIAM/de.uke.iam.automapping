from typing import Iterable, Mapping


class Preprocessor:
    """
    A step in the pipeline preprocessing the raw input.
    """

    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        raise NotImplementedError(
            "Abstract method required to be overwritten in subclass"
        )


class Abbreviations(Preprocessor):
    """
    A step in the pipeline removing abbreviations given a mapping.
    """

    def __init__(self, mapping: Mapping[str, str]):
        # You can add a static method for reading the mapping from e.g. a Excel file.
        self.mapping = mapping

    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        for sample in data:
            # Do something with sample here
            raise NotImplementedError()
            yield sample


class EntityExtractor(Preprocessor):
    """
    A step in the pipeline removing uneccessary word.
    """

    def __call__(self, data: Iterable[str]) -> Iterable[str]:
        for sample in data:
            # Do something with sample here
            raise NotImplementedError()
            yield sample
