import pandas as pd
from .base import Exporter, register_exporter

@register_exporter("snakemake_rnaseq")
class SnakemakeRNAseq(Exporter):
    def name(self) -> str: return "snakemake_rnaseq"

    def write(self, df: pd.DataFrame, out_path):
        rows = []
        for _, r in df.iterrows():
            exp = r["experiment_accession"]
            file_path = r.get("local_path") or r.get("url")
            rows.append({
                "sample": exp,
                "file": file_path,
            })
        pd.DataFrame(rows).to_csv(out_path, sep="\t", index=False)
