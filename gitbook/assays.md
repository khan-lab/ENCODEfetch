# Assay Support

ENCODEfetch supports multiple assays:

- **ChIP-seq** — full support, nf-core + Snakemake exporters
- **ATAC-seq** — placeholder classes + exporters (extensible)
- **RNA-seq** — placeholder classes + exporters (extensible)

Each assay can define its own:
- Normalization (e.g., paired FASTQ collapsing, strandedness)
- Samplesheet exporters
