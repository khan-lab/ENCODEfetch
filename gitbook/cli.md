# Command-line Usage

```bash
encodefetch --assay-title "Histone ChIP-seq"              --target-label H3K27ac              --organism "Mus musculus"              --file-type bam              --status released              --threads 8              --progress
```

## Main options

- `--accessions ENCSR123ABC,ENCSR456DEF` → Fetch specific experiments.
- `--assay-title` → TF ChIP-seq, Histone ChIP-seq, ATAC-seq, RNA-seq.
- `--target-label` → BRD4, SMAD3, H3K27ac, etc.
- `--organism` → Homo sapiens, Mus musculus.
- `--file-type` → fastq, bam, bed, bigWig, bedpe, tsv.
- `--status` → released (default), archived.
- `--perturbed true|false` → Filter perturbed experiments.
- `--threads` → Worker threads for fetching + downloads.
- `--download` → Retrieve files to `outdir/files/`.
- `--nfcore` / `--snakemake` → Export samplesheets.
- `--max-retries` / `--chunk-size` → Tune downloader reliability/throughput.
- `--version` → Show version.

Run `encode-fetch --help` for all options.
