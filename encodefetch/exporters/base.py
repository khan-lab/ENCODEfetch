from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

EXPORTER_REGISTRY: Dict[str, "Exporter"] = {}

def register_exporter(name: str):
    def deco(cls):
        EXPORTER_REGISTRY[name] = cls()
        return cls
    return deco

class Exporter(ABC):
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def write(self, df, out_path): ...
