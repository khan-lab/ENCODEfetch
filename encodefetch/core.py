from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Tuple, Set
import concurrent.futures as cf
import pandas as pd

from .encode_client import encode_get, fetch_experiment, build_params, ENCODE_BASE
from .postprocess import collapse_fastq_pairs
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    MofNCompleteColumn, TimeElapsedColumn, TimeRemainingColumn
)

def _join_list(v):
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v if x is not None and str(x) != "")
    return str(v) if v not in (None, "") else ""

def expand_possible_controls(exp_json):
    ctrls = []
    for c in exp_json.get("possible_controls", []):
        if isinstance(c, str):
            acc = c.strip("/").split("/")[-1]
        elif isinstance(c, dict):
            acc = c.get("accession") or c.get("@id", "").strip("/").split("/")[-1]
        else:
            acc = None
        if acc and acc not in ctrls:
            ctrls.append(acc)
    return ctrls

def collect_files_from_experiment(exp_json,
                                  file_types: Optional[Set[str]] = None,
                                  assembly: Optional[str] = None,
                                  status: str = "released"):
    out = []
    for f in exp_json.get("files", []):
        if status and f.get("status") != status:
            continue
        file_format = (f.get("file_format") or "").lower()
        if file_types and file_format not in file_types:
            continue
        if assembly and file_format != "fastq" and f.get("assembly") != assembly:
            continue
        out.append(f)
    return out

def build_file_record(file_json, *, exp_json, is_control, matched_controls: str = ""):
    def g(obj, key, default=""):
        return obj.get(key, default) if isinstance(obj, dict) else default

    target = g(exp_json, "target", {})
    biosample = g(exp_json, "biosample_ontology", {})
    lab = g(exp_json, "lab", {})
    award = g(exp_json, "award", {})

    donor = (
        exp_json.get("replicates", [{}])[0]
        .get("library", {})
        .get("biosample", {})
        .get("donor", {})
    )

    organ_slims         = _join_list(g(biosample, "organ_slims", []))
    cell_slims          = _join_list(g(biosample, "cell_slims", []))
    developmental_slims = _join_list(g(biosample, "developmental_slims", []))
    system_slims        = _join_list(g(biosample, "system_slims", []))
    synonyms            = _join_list(g(biosample, "synonyms", []))

    paired_with = g(file_json, "paired_with","")
    paired_accession = paired_with.split("/")[-2] if paired_with else ""

    files_url = file_json.get("href") or ""
    absolute_url = ENCODE_BASE + files_url if files_url.startswith("/") else files_url

    return {
        # Experiment-level
        "experiment_accession": g(exp_json, "accession"),
        "is_control": is_control,
        "matched_control_experiments": matched_controls,
        "control_type": g(exp_json, "control_type", ""),
        "assay_title": g(exp_json, "assay_title"),
        "description": g(exp_json, "biosample_summary"),
        "lab": g(lab, "title"),
        "award": g(award, "rfa"),
        "date_released": g(exp_json, "date_released"),
        "status_exp": g(exp_json, "status"),
        "dbxrefs": ",".join(g(exp_json, "dbxrefs", [])),
        "life_stage_age": g(exp_json, "life_stage_age", ""),
        "perturbed": g(exp_json, "perturbed", ""),

        # Donor
        "donor_accession": donor.get("accession", ""),
        "donor_sex": donor.get("sex", ""),
        "donor_life_stage": donor.get("life_stage", ""),
        "donor_age": donor.get("age", ""),
        "donor_age_units": donor.get("age_units", ""),
        "donor_ethnicity": (", ".join(donor.get("ethnicity", [])) if isinstance(donor.get("ethnicity"), list) else donor.get("ethnicity","")),
        "organism": donor.get("organism", {}).get("scientific_name", ""),

        # Biosample-ontology
        "biosample_term_id":   g(biosample, "term_id"),
        "biosample_term_name": g(biosample, "term_name"),
        "classification":      g(biosample, "classification"),
        "organ_slims":         organ_slims,
        "cell_slims":          cell_slims,
        "developmental_slims": developmental_slims,
        "system_slims":        system_slims,
        "biosample_synonyms":  synonyms,

        # Target
        "target_label": g(target, "label"),
        "target_title": g(target, "title"),

        # File
        "file_accession": g(file_json, "accession"),
        "file_format": g(file_json, "file_format"),
        "output_type": g(file_json, "output_type"),
        "assembly": g(file_json, "assembly"),
        "run_type": g(file_json, "run_type"),
        "paired_end": g(file_json, "paired_end"),
        "paired_accession": paired_accession,
        "md5sum": g(file_json, "md5sum"),
        "file_status": g(file_json, "status"),
        "file_size": g(file_json, "file_size"),
        "platform": g(file_json, "platform", {}).get("term_name", ""),

        # Replicates
        "bio_replicate_count": g(exp_json, "bio_replicate_count", ""),
        "tech_replicate_count": g(exp_json, "tech_replicate_count", ""),
        "biological_replicates": ",".join(map(str, g(file_json, "biological_replicates", []))),
        "technical_replicates": ",".join(map(str, g(file_json, "technical_replicates", []))),
        "biological_replicates_formatted": g(file_json, "biological_replicates_formatted", ""),
        "replication_type": g(exp_json, "replication_type", ""),

        # Links
        "url": absolute_url,
    }

def experiments_to_df(experiments: Iterable[dict],
                      file_types: Optional[Set[str]] = None,
                      assembly: Optional[str] = None,
                      status: str = "released",
                      auth_token: Optional[str] = None,
                      progress: bool = False,
                      threads: int = 6,
                      ) -> Tuple[pd.DataFrame, List[dict]]:
    
    auth = (auth_token, "") if auth_token else None
    seen, cases = set(), []
    for exp in experiments:
        acc = exp.get("accession")
        if not acc or acc in seen:
            continue
        seen.add(acc)
        cases.append(exp)

    rows: List[dict] = []

    def process_experiment(exp) -> List[dict]:
        local_rows: List[dict] = []
        exp_acc = exp.get("accession")
        print(f"📦 Fetching experiment: {exp_acc}")
        exp_full = fetch_experiment(exp_acc, auth=auth, embedded=True)
        ctrl_list = expand_possible_controls(exp_full)
        ctrls_csv = ",".join(ctrl_list)

        # case files
        for f in collect_files_from_experiment(exp_full, file_types=file_types, assembly=assembly, status=status):
            local_rows.append(build_file_record(f, exp_json=exp_full, is_control=False, matched_controls=ctrls_csv))

        # control files (fetched serially inside this worker)
        for cacc in ctrl_list:
            try:
                ctrl_exp = fetch_experiment(cacc, auth=auth, embedded=True)
                for f in collect_files_from_experiment(ctrl_exp, file_types=file_types, assembly=assembly, status=status):
                    local_rows.append(build_file_record(f, exp_json=ctrl_exp, is_control=True, matched_controls=""))
            except Exception as e:
                print(f"  ⚠️  Failed to fetch control {cacc}: {e}")

        return local_rows

    if progress:
        columns = [
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        ]

        with Progress(*columns) as prog, ThreadPoolExecutor(max_workers=threads) as ex:
            task = prog.add_task("Experiments", total=len(cases))
            futures = [ex.submit(process_experiment, exp) for exp in cases]
            for fut in as_completed(futures):
                rows.extend(fut.result())
                prog.update(task, advance=1)
    else:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            for fut in as_completed([ex.submit(process_experiment, exp) for exp in cases]):
                rows.extend(fut.result())

    if not rows:
        return pd.DataFrame(), []
    df = pd.DataFrame(rows).sort_values(
        ["is_control", "experiment_accession", "file_accession"]
    )
    return df, rows

def search_experiments(assay_title: Optional[str] = None,
                       target_labels: Optional[List[str]] = None,
                       organism: Optional[str] = None,
                       file_types: Optional[Set[str]] = None,
                       assembly: Optional[str] = None,
                       status: str = "released",
                       auth_token: Optional[str] = None,
                       progress: bool = False,
                       perturbed: Optional[str] = None,
                       threads: int = 6,):
    auth = (auth_token, "") if auth_token else None
    params_list = build_params(
        assay_title=assay_title,
        target_labels=target_labels,
        organism=organism,
        status=status,
        perturbed=perturbed,
    )
    res = encode_get("/search/", params=params_list, auth=auth, raw_query="control_type!=*")
    experiments = res.get("@graph", [])
    print(f"🔢 Found {len(experiments)} experiment(s) to fetch.\n")
    return experiments_to_df(experiments, file_types=file_types, assembly=assembly, status=status,
                             auth_token=auth_token, progress=progress, threads=threads)

def search_accessions(accessions: List[str],
                      file_types: Optional[Set[str]] = None,
                      assembly: Optional[str] = None,
                      status: str = "released",
                      auth_token: Optional[str] = None,
                      progress: bool = False,
                      threads: int = 6,):
    auth = (auth_token, "") if auth_token else None
    experiments = [fetch_experiment(acc.strip(), auth=auth) for acc in accessions if acc.strip()]
    return experiments_to_df(experiments, file_types=file_types, assembly=assembly, status=status,
                             auth_token=auth_token, progress=progress, threads=threads)

def ensure_dir(p: Path): p.mkdir(parents=True, exist_ok=True)

def download_file(
    url: str,
    dest_path: Path,
    *,
    progress,          # rich.progress.Progress instance
    task_id: int,      # task created for this file
    auth=None,
    chunk: int = 1024 * 1024,
    retries: int = 3,
    sleep: int = 1,
) -> bool:
    import requests, time
    # ensure dir
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest_path.with_suffix(dest_path.suffix + ".part")

    headers = {}
    # Resume support
    pos = tmp.stat().st_size if tmp.exists() else 0
    if pos:
        headers["Range"] = f"bytes={pos}-"
        progress.update(task_id, completed=pos)

    for _ in range(retries):
        try:
            with requests.get(url, headers=headers, stream=True, auth=auth, timeout=60) as r:
                if r.status_code in (200, 206):
                    mode = "ab" if pos else "wb"
                    with open(tmp, mode) as f:
                        for chunk_data in r.iter_content(chunk_size=chunk):
                            if not chunk_data:
                                continue
                            f.write(chunk_data)
                            progress.update(task_id, advance=len(chunk_data))
                    tmp.replace(dest_path)
                    progress.update(task_id, completed=progress.tasks[task_id].total or progress.tasks[task_id].completed)
                    return True
                else:
                    time.sleep(sleep)
        except Exception:
            time.sleep(sleep)
    return False


def write_nfcore_sheet(df: pd.DataFrame, outpath: Path):
    from .exporters.nfcore_chipseq import NFCoreChipseq
    NFCoreChipseq().write(df, outpath)

def write_snakemake_sheet(df: pd.DataFrame, outpath: Path):
    from .exporters.snakemake_chipseq import SnakemakeChipseq
    SnakemakeChipseq().write(df, outpath)
