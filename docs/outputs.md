# Outputs

A run writes a reproducible output directory. By default this is `encode_results/`; change it with `--outdir`.

## Directory layout

```text
encode_results/
  manifest.tsv
  metadata.jsonl
  files/
    case/
      ENCSR...
        ENCFF....fastq.gz
    control/
      ENCSR...
        ENCFF....fastq.gz
  nfcore_*_samplesheet.csv
  snakemake_*_samplesheet.csv
```

`files/` is created only when downloads are enabled. With `--metadata-only`, ENCODEfetch writes metadata and samplesheets without downloading files.

## manifest.tsv

`manifest.tsv` is the main tidy table. It contains one row per matched file before FASTQ collapsing, or one row per pair after `collapse_fastq_pairs`.

Important columns include:

| Column | Description |
| --- | --- |
| `experiment_accession` | ENCODE experiment accession. |
| `is_control` | `True` for matched control experiments, `False` for case experiments. |
| `matched_control_experiments` | Comma-separated experiment-level controls from ENCODE `possible_controls`. |
| `controlled_by_files` | Normalized file accessions from ENCODE file-level `controlled_by` links. |
| `assay_title` | ENCODE assay title. |
| `target_label` | Target label for ChIP-style assays. |
| `organism` | Donor organism scientific name. |
| `biosample_term_name` | Biosample ontology term name. |
| `file_accession` | ENCODE file accession. |
| `file_format` | File format such as `fastq`, `bam`, `bed`, or `bigWig`. |
| `output_type` | ENCODE output type. |
| `assembly` | Genome assembly where applicable. |
| `md5sum` | ENCODE file checksum. |
| `file_size` | File size in bytes. |
| `url` | Absolute ENCODE download URL. |
| `local_path` | Local downloaded file path, when downloads are performed. |

After FASTQ collapsing, additional helper columns can include `fastq_1`, `fastq_2`, `single_end`, `file_accession_r2`, `local_path_r2`, and `url_r2`.

## metadata.jsonl

`metadata.jsonl` stores one JSON object per record. It is useful for audit trails and downstream tools that prefer line-delimited JSON.

## Samplesheets

Samplesheets are written only when requested:

- `--nfcore` writes `nfcore_*_samplesheet.csv`.
- `--snakemake` writes `snakemake_*_samplesheet.csv`.

Samplesheet rows prefer local downloaded paths when they are available, then fall back to remote URLs.
