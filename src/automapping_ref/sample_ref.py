from dataclasses import dataclass
from .language_ref import Language


@dataclass
class Sample:
    """
    A sample of data for mapping to medical ontologies.
    """

    id: str
    content: str
    language: Language
