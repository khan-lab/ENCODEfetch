# Python API

```python
import encodefetch as ef

# Search ENCODE
df, records = ef.search_experiments(
    assay_title="TF ChIP-seq",
    target_labels=["BRD4","SMAD3"],
    organism="Homo sapiens",
    file_types={"fastq"},
    status="released",
    threads=8,
    progress=True,
)

print(df.head())

# Collapse paired-end FASTQs
df2 = ef.collapse_fastq_pairs(df)

# nf-core samplesheet (ChIP-seq)
ef.write_nfcore_sheet(df2, "nfcore_chipseq.csv")
```
