# Python API

Import ENCODEfetch as a Python package when you want to work in notebooks, scripts, or larger workflow code.

```python
import encodefetch as ef
```

## Search experiments

```python
df, records = ef.search_experiments(
    assay_title="TF ChIP-seq",
    target_labels=["BRD4", "SMAD3"],
    organism="Homo sapiens",
    biosample=None,
    file_types={"fastq"},
    assembly=None,
    status="released",
    perturbed="false",
    series="OrganismDevelopmentSeries",
    progress=True,
    threads=8,
)
```

Returns:

- `df`: a tidy `pandas.DataFrame` with one row per matched file before FASTQ collapsing.
- `records`: a list of dictionaries used to write `metadata.jsonl`.

## Search accessions

```python
df, records = ef.search_accessions(
    ["ENCSR514EOE", "ENCSR395MHA"],
    file_types={"fastq"},
    status="released",
    progress=False,
    threads=4,
)
```

## Collapse paired FASTQs

```python
df = ef.collapse_fastq_pairs(df)
```

For paired-end FASTQs, this keeps one row for a pair and adds helper columns such as `fastq_1`, `fastq_2`, `single_end`, and `file_accession_r2`.

## Write samplesheets

```python
ef.write_nfcore_sheet(
    df,
    "TF ChIP-seq",
    "nfcore_tf_chipseq_samplesheet.csv",
    control_strategy="all",
)

ef.write_snakemake_sheet(
    df,
    "TF ChIP-seq",
    "snakemake_tf_chipseq_samplesheet.tsv",
    control_strategy="pool",
)
```

The assay title determines which exporter is used.

## Public functions

| Function | Purpose |
| --- | --- |
| `search_experiments(...)` | Search ENCODE using assay, target, organism, biosample, status, perturbation, series, file type, and assembly filters. |
| `search_accessions(...)` | Fetch one or more known ENCODE experiment accessions. |
| `experiments_to_df(...)` | Convert ENCODE experiment JSON objects into a manifest DataFrame and metadata records. |
| `collapse_fastq_pairs(df)` | Collapse paired-end FASTQ records into single rows with R1/R2 columns. |
| `write_nfcore_sheet(df, assay_title, outpath, control_strategy="all")` | Write an assay-aware nf-core samplesheet. |
| `write_snakemake_sheet(df, assay_title, outpath, control_strategy="all")` | Write an assay-aware Snakemake samplesheet. |

## Authentication

Pass an ENCODE token through `auth_token`:

```python
df, records = ef.search_experiments(
    assay_title="RNA-seq",
    organism="Homo sapiens",
    file_types={"fastq"},
    auth_token="YOUR_TOKEN",
)
```
