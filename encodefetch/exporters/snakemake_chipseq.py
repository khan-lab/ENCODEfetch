import pandas as pd
from .base import Exporter, register_exporter

@register_exporter("snakemake_chipseq")
class SnakemakeChipseq(Exporter):
    def name(self) -> str: return "snakemake_chipseq"

    def write(self, df: pd.DataFrame, out_path):
        rows = []
        for _, r in df.iterrows():
            exp = r["experiment_accession"]
            rep = (r.get("biological_replicates") or "1").split(",")[0].strip()
            group = "control" if r.get("is_control") else "case"
            file_path = r.get("local_path") or r.get("url")
            rows.append({
                "sample": exp,
                "group": group,
                "replicate": rep,
                "file": file_path,
            })
        pd.DataFrame(rows).to_csv(out_path, sep="\t", index=False)
