from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
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

def _same_value(left, right) -> bool:
    left = first_present(left)
    right = first_present(right)
    return bool(left and right and left.lower() == right.lower())

def _candidate_rows(df, control: str):
    if df is None or not control:
        return []

    rows = []
    for _, row in df.iterrows():
        if "is_control" in row and not row.get("is_control"):
            continue
        if str(row.get("experiment_accession", "")) == control:
            rows.append(row)
            continue
        if str(row.get("file_accession", "")) == control:
            rows.append(row)
    return rows

def _control_score(case_row, control_row) -> int:
    score = 0
    weighted_fields: List[Tuple[str, int]] = [
        ("biosample_term_id", 50),
        ("biosample_term_name", 35),
        ("organism", 25),
        ("lab", 15),
        ("award", 10),
        ("classification", 10),
        ("biological_replicates", 10),
        ("run_type", 8),
        ("technical_replicates", 5),
        ("donor_sex", 5),
        ("donor_life_stage", 5),
        ("paired_end", 5),
        ("file_format", 5),
    ]
    for field, weight in weighted_fields:
        if _same_value(case_row.get(field), control_row.get(field)):
            score += weight

    if _same_value(control_row.get("file_status"), "released"):
        score += 5
    if first_present(
        control_row.get("fastq_1"),
        control_row.get("local_path"),
        control_row.get("url"),
    ):
        score += 3
    return score

def best_control_for_row(controls: List[str], case_row=None, df=None) -> str:
    if not controls:
        return ""
    if case_row is None or df is None:
        return controls[0]

    best_control = controls[0]
    best_score: Optional[int] = None
    for control in controls:
        rows = _candidate_rows(df, control)
        score = max((_control_score(case_row, row) for row in rows), default=0)
        if best_score is None or score > best_score:
            best_control = control
            best_score = score
    return best_control

def controls_for_strategy(controls: List[str], strategy: str, case_row=None, df=None) -> List[str]:
    strategy = (strategy or "all").lower()
    if not controls:
        return [""]
    if strategy == "pool":
        return [";".join(controls)]
    if strategy == "first":
        return [controls[0]]
    if strategy == "best":
        return [best_control_for_row(controls, case_row=case_row, df=df)]
    return controls
