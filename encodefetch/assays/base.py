from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

ASSAY_REGISTRY: Dict[str, "Assay"] = {}

def register_assay(name: str):
    def deco(cls):
        ASSAY_REGISTRY[name] = cls()
        return cls
    return deco

class Assay(ABC):
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def normalize(self, df):
        "Assay-specific postprocessing (e.g., collapse paired fastqs)."
        ...
    def default_file_types(self) -> set[str]:
        return set()
    def exporter_ids(self) -> list[str]:
        return []
