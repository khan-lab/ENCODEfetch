from .base import Assay, register_assay
from ..postprocess import collapse_fastq_pairs

@register_assay("ATAC-seq")
class ATACSeq(Assay):
    def name(self) -> str: return "ATAC-seq"
    def normalize(self, df):
        if "file_format" in df and df["file_format"].astype(str).str.lower().eq("fastq").any():
            return collapse_fastq_pairs(df)
        return df
    def default_file_types(self) -> set[str]:
        return {"fastq"}
    def exporter_ids(self) -> list[str]:
        return ["nfcore_atacseq", "snakemake_atacseq"]
