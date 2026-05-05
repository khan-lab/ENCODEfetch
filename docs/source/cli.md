# Command-line Interface

Basic example:

```bash
encodefetch --assay-title "TF ChIP-seq"              --target-label BRD4,SMAD3              --organism "Homo sapiens"              --file-type fastq              --status released              --progress              --threads 8              --nfcore
```

Run `encodefetch --help` to see all options.

## Key options

- `--accessions ENCSR123ABC,ENCSR456DEF` — fetch experiments by accession directly.
- `--accessions accessions.txt` — read one experiment accession per line; blank lines and `#` comments are ignored.
- `--assay-title` — e.g. `TF ChIP-seq`, `Histone ChIP-seq`, `ATAC-seq`, `RNA-seq`.
- `--target-label` — one or more targets (comma-separated).
- `--organism` — e.g. `Homo sapiens`, `Mus musculus`.
- `--file-type` — restrict formats (`fastq`, `bam`, `bed`, `bigWig`…).
- `--status` — default `released`.
- `--perturbed true|false` — filter perturbed experiments.
- `--series OrganismDevelopmentSeries` — filter experiments by related ENCODE series `@type`.
- `--threads` — max workers for metadata fetching, control fetching, and downloads.
- `--metadata-only` — skip file downloads and write metadata/sample sheets only.
- `--max-retries` / `--chunk-size` — tune downloader retry count and streamed chunk size.
- `--nfcore` / `--snakemake` — export sample sheets.
- `--control-strategy all|pool|best` — choose how samplesheets represent multiple controls.

The manifest always preserves all matched controls in `matched_control_experiments` and adds file-level `controlled_by_files` when ENCODE provides `controlled_by` links. The control strategy only changes samplesheet output.
