import pandas as pd
from .base import Exporter, register_exporter

@register_exporter("nfcore_chipseq")
class NFCoreChipseq(Exporter):
    def name(self) -> str: return "nfcore_chipseq"

    def write(self, df: pd.DataFrame, out_path):
        fq = df[df["file_format"].astype(str).str.lower().eq("fastq")] if "file_format" in df else df
        rows = []
        for _, r in fq.iterrows():
            exp = r["experiment_accession"]
            rep = (r.get("biological_replicates") or "1").split(",")[0].strip()
            rows.append({
                "sample": exp,
                "fastq_1": r.get("fastq_1",""),
                "fastq_2": r.get("fastq_2",""),
                "single_end": r.get("single_end",""),
                "antibody": r.get("target_label",""),
                "replicate": rep,
                "control": r.get("matched_control_experiments","") if not r.get("is_control") else "",
                "control_replicate": rep if not r.get("is_control") else "",
            })
        pd.DataFrame(rows).to_csv(out_path, index=False)
