# Changelog

## 0.5.0

- Added accession-file parsing for `--accessions`.
- Added metadata-only mode as the preferred way to skip downloads.
- Added exporter control strategies: `all`, `pool`, and `best`.
- Improved file-level control mapping through `controlled_by_files`.
- Added nf-core and Snakemake exporters for ChIP-seq, ATAC-seq, and RNA-seq assay families.

## 0.1.0

- Initial release.
- Experiment-first search with control expansion.
- Multi-threaded metadata fetching and downloads.
- Paired FASTQ collapsing.
- nf-core and Snakemake samplesheet exporters.
- Rich progress bars for experiments and downloads.
