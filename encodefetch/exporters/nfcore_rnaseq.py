import pandas as pd
from .base import Exporter, register_exporter

@register_exporter("nfcore_rnaseq")
class NFCoreRNAseq(Exporter):
    def name(self) -> str: return "nfcore_rnaseq"

    def write(self, df: pd.DataFrame, out_path):
        fq = df[df["file_format"].astype(str).str.lower().eq("fastq")] if "file_format" in df else df
        rows = []
        for _, r in fq.iterrows():
            exp = r["experiment_accession"]
            rows.append({
                "sample": exp,
                "fastq_1": r.get("fastq_1",""),
                "fastq_2": r.get("fastq_2",""),
                "single_end": r.get("single_end",""),
                "strandedness": "",
            })
        pd.DataFrame(rows).to_csv(out_path, index=False)
