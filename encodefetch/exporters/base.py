from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

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
    def write(self, df, out_path, control_strategy: str = "all"): ...

def split_csv(value) -> List[str]:
    if value is None:
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]

def first_present(*values) -> str:
    for value in values:
        if value is None:
            continue
        if pd.isna(value):
            continue
        value = str(value).strip()
        if value:
            return value
    return ""

def control_file_to_sample_map(df) -> Dict[str, str]:
    if "file_accession" not in df or "experiment_accession" not in df:
        return {}
    mapping: Dict[str, str] = {}
    for _, row in df.iterrows():
        if "is_control" in row and not row.get("is_control"):
            continue
        file_acc = row.get("file_accession")
        exp_acc = row.get("experiment_accession")
        if file_acc and exp_acc and file_acc not in mapping:
            mapping[str(file_acc)] = str(exp_acc)
    return mapping

def resolve_controls_for_row(row, file_to_sample: Dict[str, str]) -> List[str]:
    controls: List[str] = []
    controlled_by_files = split_csv(row.get("controlled_by_files", ""))
    if controlled_by_files:
        for file_acc in controlled_by_files:
            controls.append(file_to_sample.get(file_acc, file_acc))
    else:
        controls.extend(split_csv(row.get("matched_control_experiments", "")))

    out: List[str] = []
    seen = set()
    for control in controls:
        if control and control not in seen:
            seen.add(control)
            out.append(control)
    return out

def controls_for_strategy(controls: List[str], strategy: str) -> List[str]:
    strategy = (strategy or "all").lower()
    if not controls:
        return [""]
    if strategy == "pool":
        return [";".join(controls)]
    if strategy == "best":
        # TODO: rank controls by biosample, replicate, and file quality metadata.
        return [controls[0]]
    return controls
