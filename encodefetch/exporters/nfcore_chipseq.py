import pandas as pd
from .base import Exporter, register_exporter, control_file_to_sample_map, resolve_controls_for_row, controls_for_strategy

@register_exporter("nfcore_chipseq")
class NFCoreChipseq(Exporter):
    def name(self) -> str: return "nfcore_chipseq"

    def write(self, df: pd.DataFrame, out_path, control_strategy: str = "all"):
        fq = df[df["file_format"].astype(str).str.lower().eq("fastq")] if "file_format" in df else df
        file_to_sample = control_file_to_sample_map(df)
        rows = []
        for _, r in fq.iterrows():
            exp = r["experiment_accession"]
            rep = (r.get("biological_replicates") or "1").split(",")[0].strip()
            controls = [] if r.get("is_control") else resolve_controls_for_row(r, file_to_sample)
            for control in controls_for_strategy(controls, control_strategy, case_row=r, df=df):
                rows.append({
                    "sample": exp,
                    "fastq_1": r.get("fastq_1",""),
                    "fastq_2": r.get("fastq_2",""),
                    #"single_end": r.get("single_end",""),
                    "replicate": rep,
                    "antibody": r.get("target_label",""),
                    "control": control,
                    "control_replicate": rep if control else "",
                })
        pd.DataFrame(rows).to_csv(out_path, index=False)
