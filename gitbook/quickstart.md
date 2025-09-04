# Quickstart

Fetch BRD4 ChIP-seq data and matched controls:

```bash
encodefetch --assay-title "TF ChIP-seq"              --target-label BRD4              --organism "Homo sapiens"              --file-type fastq              --status released              --progress              --download
```

This will:

1. Search ENCODE for matching experiments.
2. Expand `possible_controls` for each case.
3. Write `manifest.tsv` and `metadata.jsonl`.
4. Download FASTQs into `files/`.
