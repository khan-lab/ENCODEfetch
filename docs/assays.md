# Assays

ENCODEfetch keeps assay-aware behavior small and explicit. Search can use any ENCODE assay title, while samplesheet export is currently mapped for the assay families below.

## Supported exporter families

| Family | Assay titles recognized for export |
| --- | --- |
| TF binding and ChIP-seq | `TF ChIP-seq`, `ChIP-seq`, `Histone ChIP-seq` |
| Transcriptome | `RNA-seq`, `total RNA-seq`, `long RNA-seq`, `polyA plus RNA-seq`, `polyA minus RNA-seq`, `small RNA-seq` |
| DNA accessibility | `ATAC-seq`, `DNase-seq`, `snATAC-seq`, `FAIRE-seq`, `MNase-seq` |

## ChIP-seq

ChIP-seq export includes target antibody information and matched controls.

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --snakemake
```

## ATAC-seq

ATAC-seq export writes case/control FASTQ samplesheets for nf-core/atacseq-style and Snakemake workflows.

```bash
encodefetch \
  --assay-title "ATAC-seq" \
  --organism "Homo sapiens" \
  --file-type fastq \
  --metadata-only \
  --nfcore
```

## RNA-seq

RNA-seq export writes strandedness and sequencing platform fields. If strandedness is not available, exporters use `auto`.

```bash
encodefetch \
  --assay-title "RNA-seq" \
  --organism "Homo sapiens" \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --snakemake
```

## Adding an assay

New assay behavior usually needs:

- An assay class under `encodefetch/assays/` if normalization differs.
- An exporter under `encodefetch/exporters/`.
- A mapping in `write_nfcore_sheet` or `write_snakemake_sheet`.
- Tests that assert the generated samplesheet columns and representative rows.
