# Command-line Interface

Basic example:

```bash
encodefetch --assay-title "TF ChIP-seq"              --target-label BRD4,SMAD3              --organism "Homo sapiens"              --file-type fastq              --status released              --progress              --download              --threads 8              --nfcore
```

Run `encodefetch --help` to see all options.

## Key options

- `--accessions ENCSR123ABC,ENCSR456DEF` — fetch experiments by accession directly.
- `--assay-title` — e.g. `TF ChIP-seq`, `Histone ChIP-seq`, `ATAC-seq`, `RNA-seq`.
- `--target-label` — one or more targets (comma-separated).
- `--organism` — e.g. `Homo sapiens`, `Mus musculus`.
- `--file-type` — restrict formats (`fastq`, `bam`, `bed`, `bigWig`…).
- `--status` — default `released`.
- `--perturbed true|false` — filter perturbed experiments.
- `--threads` — max workers for metadata fetching and downloads.
- `--download` — retrieve matched files to `outdir/files/`.
- `--nfcore` / `--snakemake` — export sample sheets.
