# Usage (Python API)

```python
import encodefetch as ef

# Search experiments
df, recs = ef.search_experiments(
    assay_title="TF ChIP-seq",
    target_labels=["BRD4","SMAD3"],
    organism="Homo sapiens",
    file_types={"fastq"},
    status="released",
    perturbed="false",
    progress=True,
    threads=8,
)

# Collapse paired-end FASTQs to a single row per sample
df2 = ef.collapse_fastq_pairs(df)

# Export to nf-core samplesheet
# ef.write_samplesheet(df2, "nfcore_chipseq", "nfcore_chipseq.csv")
```
