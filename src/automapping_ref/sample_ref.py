from dataclasses import dataclass, field
from language_ref import Language
from prediction_ref import Prediction
from typing import List


@dataclass
class Sample:
    """
    A sample of data for mapping to medical ontologies.
    """

    id: str
    content: str
    language: Language
    concepts: List[Prediction] = field(default_factory=list)
