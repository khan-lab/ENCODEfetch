# Outputs

A typical run generates:

- **`manifest.tsv`** — tidy metadata table (one row per file; FASTQs can be collapsed to R1/R2).
- **`metadata.jsonl`** — JSON lines of file records.
- **`files/`** — downloaded case/control files with directory structure.
- **`nfcore_*_samplesheet.csv`** — nf-core pipeline samplesheet(s).
- **`snakemake_samples.tsv`** — Snakemake sample table.

Key columns in `manifest.tsv` include:
- `experiment_accession`, `is_control`, `matched_control_experiments`
- `assay_title`, `target_label`, `organism`
- `biosample_term_name`, `biosample_term_id`, `classification`
- File fields: `file_accession`, `file_format`, `output_type`, `md5sum`, `file_size`
- FASTQ helpers (after collapsing): `fastq_1`, `fastq_2`, `single_end`, `file_accession_r2`
