import pandas as pd
from .base import Exporter, register_exporter, first_present
from .nfcore_rnaseq import _seq_platform

@register_exporter("snakemake_rnaseq")
class SnakemakeRNAseq(Exporter):
    def name(self) -> str: return "snakemake_rnaseq"

    def write(self, df: pd.DataFrame, out_path, control_strategy: str = "all"):
        fq = df[df["file_format"].astype(str).str.lower().eq("fastq")] if "file_format" in df else df
        rows = []
        for _, r in fq.iterrows():
            exp = r["experiment_accession"]
            rep = (r.get("biological_replicates") or "1").split(",")[0].strip()
            rows.append({
                "sample": exp,
                "replicate": rep,
                "fastq_1": first_present(r.get("fastq_1"), r.get("local_path"), r.get("url")),
                "fastq_2": first_present(r.get("fastq_2"), r.get("local_path_r2"), r.get("url_r2")),
                "strandedness": r.get("strandedness", "") or "auto",
                "seq_platform": _seq_platform(r.get("platform", "")),
            })
        pd.DataFrame(rows).to_csv(out_path, sep="\t", index=False)
