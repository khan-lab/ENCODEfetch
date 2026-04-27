import pandas as pd
from .base import (
    Exporter,
    register_exporter,
    first_present,
    control_file_to_sample_map,
    resolve_controls_for_row,
    controls_for_strategy,
)

@register_exporter("snakemake_atacseq")
class SnakemakeATACseq(Exporter):
    def name(self) -> str: return "snakemake_atacseq"

    def write(self, df: pd.DataFrame, out_path, control_strategy: str = "all"):
        fq = df[df["file_format"].astype(str).str.lower().eq("fastq")] if "file_format" in df else df
        file_to_sample = control_file_to_sample_map(df)
        rows = []
        for _, r in fq.iterrows():
            exp = r["experiment_accession"]
            rep = (r.get("biological_replicates") or "1").split(",")[0].strip()
            group = "control" if r.get("is_control") else "case"
            fastq_1 = first_present(r.get("fastq_1"), r.get("local_path"), r.get("url"))
            fastq_2 = first_present(r.get("fastq_2"), r.get("local_path_r2"), r.get("url_r2"))
            controls = [] if r.get("is_control") else resolve_controls_for_row(r, file_to_sample)
            for control in controls_for_strategy(controls, control_strategy):
                rows.append({
                    "sample": exp,
                    "group": group,
                    "replicate": rep,
                    "fastq_1": fastq_1,
                    "fastq_2": fastq_2,
                    "control": control,
                    "control_replicate": rep if control else "",
                })
        pd.DataFrame(rows).to_csv(out_path, sep="\t", index=False)
