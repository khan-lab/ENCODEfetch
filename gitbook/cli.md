# Command-line Usage

```bash
encodefetch --assay-title "Histone ChIP-seq"              --target-label H3K27ac              --organism "Mus musculus"              --file-type bam              --status released              --threads 8              --progress
```

## Main options

- `--accessions ENCSR123ABC,ENCSR456DEF` → Fetch specific experiments.
- `--accessions accessions.txt` → Read one accession per line; blank lines and `#` comments are ignored.
- `--assay-title` → TF ChIP-seq, Histone ChIP-seq, ATAC-seq, RNA-seq.
- `--target-label` → BRD4, SMAD3, H3K27ac, etc.
- `--organism` → Homo sapiens, Mus musculus.
- `--file-type` → fastq, bam, bed, bigWig, bedpe, tsv.
- `--status` → released (default), archived.
- `--perturbed true|false` → Filter perturbed experiments.
- `--series OrganismDevelopmentSeries` → Filter experiments by related ENCODE series `@type`.
- `--threads` → Worker threads for metadata fetching, control fetching, and downloads.
- `--metadata-only` → Skip file downloads and write metadata/sample sheets only.
- `--nfcore` / `--snakemake` → Export samplesheets.
- `--control-strategy all|pool|best` → Choose how samplesheets represent multiple controls.
- `--max-retries` / `--chunk-size` → Tune downloader reliability/throughput.
- `--version` → Show version.

The manifest always preserves all matched controls in `matched_control_experiments` and adds file-level `controlled_by_files` when ENCODE provides `controlled_by` links. The control strategy only changes samplesheet output.

Run `encodefetch --help` for all options.
