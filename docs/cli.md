# Command Line

The console entry point is available as both `encodefetch` and `ENCODEfetch`.

```bash
encodefetch --help
```

## Search by filters

```bash
encodefetch \
  --assay-title "Histone ChIP-seq" \
  --target-label H3K27ac \
  --organism "Mus musculus" \
  --file-type bam \
  --status released \
  --metadata-only \
  --threads 8
```

## Search by accession

```bash
encodefetch \
  --accessions ENCSR514EOE,ENCSR395MHA \
  --file-type fastq \
  --metadata-only \
  --nfcore
```

## Options

| Option | Purpose |
| --- | --- |
| `--accessions` | Comma-separated experiment accessions, or a text file with one accession per line. |
| `--assay-title` | ENCODE assay title, such as `TF ChIP-seq`, `Histone ChIP-seq`, `ATAC-seq`, or `RNA-seq`. |
| `--target-label` | Target label. Repeat the option for multiple targets. |
| `--organism` | Organism scientific name, for example `Homo sapiens` or `Mus musculus`. |
| `--biosample` | Biosample ontology term name. |
| `--file-type` | File formats to include: `fastq`, `bam`, `bed`, `bigWig`, `tsv`, `bw`, or `bedpe`. |
| `--assembly` | Genome assembly filter for non-FASTQ files. |
| `--status` | File status filter. Defaults to `released`. |
| `--perturbed` | Filter experiments by perturbation state with `true` or `false`. |
| `--series` | Filter experiments by related ENCODE series `@type`, such as `OrganismDevelopmentSeries`. |
| `--outdir` | Output directory. Defaults to `encode_results`. |
| `--metadata-only` | Write metadata and samplesheets only; skip downloads. |
| `--threads` | Worker count for metadata fetching, control fetching, and downloads. |
| `--max-retries` | Maximum HTTP retries per file during download. |
| `--chunk-size` | Download chunk size in bytes. |
| `--auth-token` | ENCODE API token. |
| `--progress` / `--no-progress` | Enable or disable progress bars. |
| `--nfcore` | Write an nf-core samplesheet for the selected assay. |
| `--snakemake` | Write a Snakemake samplesheet for the selected assay. |
| `--control-strategy` | Choose `all`, `pool`, `best`, or `first` for multiple controls in samplesheets. |
| `--dry-run` | Deprecated alias for `--metadata-only`. |
| `--version` | Show the installed version. |

## Notes

The manifest always preserves all matched controls in `matched_control_experiments`. When ENCODE provides file-level control relationships, ENCODEfetch stores normalized control file accessions in `controlled_by_files`.

`--control-strategy` changes only samplesheet output:

- `all`: write one case row per resolved control.
- `pool`: write one case row with controls joined by semicolons.
- `first`: write one case row with the first resolved control.
- `best`: write one case row with the highest-scoring control based on biosample, organism, lab, replicate, file, and release metadata.

See [Exporters](exporters.md#control-strategies) for the full ranking details.
