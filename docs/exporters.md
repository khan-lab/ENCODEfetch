# Exporters

ENCODEfetch writes pipeline-ready samplesheets after the manifest has been built. The same exporter logic is available from the CLI and Python API.

## CLI usage

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --organism "Homo sapiens" \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --snakemake \
  --control-strategy all
```

## Nextflow and nf-core

Use `--nfcore` to write an nf-core samplesheet. Output file names include the assay title, for example:

- `nfcore_tf_chip-seq_samplesheet.csv`
- `nfcore_histone_chip-seq_samplesheet.csv`
- `nfcore_atac-seq_samplesheet.csv`
- `nfcore_rna-seq_samplesheet.csv`

Supported nf-core exporters:

| Assay family | Exporter | Columns |
| --- | --- | --- |
| TF ChIP-seq, Histone ChIP-seq, ChIP-seq | `NFCoreChipseq` | `sample`, `fastq_1`, `fastq_2`, `replicate`, `antibody`, `control`, `control_replicate` |
| ATAC-seq and related accessibility assays | `NFCoreATACseq` | `sample`, `fastq_1`, `fastq_2`, `replicate`, `control`, `control_replicate` |
| RNA-seq and related transcriptome assays | `NFCoreRNAseq` | `sample`, `fastq_1`, `fastq_2`, `strandedness`, `seq_platform` |

Run the generated CSV with the appropriate nf-core pipeline. For example:

```bash
nextflow run nf-core/chipseq \
  --input encode_results/nfcore_tf_chip-seq_samplesheet.csv \
  --outdir nfcore_chipseq_results \
  -profile docker
```

```bash
nextflow run nf-core/atacseq \
  --input encode_results/nfcore_atac-seq_samplesheet.csv \
  --outdir nfcore_atacseq_results \
  -profile docker
```

```bash
nextflow run nf-core/rnaseq \
  --input encode_results/nfcore_rna-seq_samplesheet.csv \
  --outdir nfcore_rnaseq_results \
  -profile docker
```

## Snakemake

Use `--snakemake` to write a tab-separated samplesheet.

Supported Snakemake exporters:

| Assay family | Exporter | Columns |
| --- | --- | --- |
| TF ChIP-seq, Histone ChIP-seq, ChIP-seq | `SnakemakeChipseq` | `sample`, `group`, `replicate`, `fastq_1`, `fastq_2`, `control`, `control_replicate`, `antibody` |
| ATAC-seq and related accessibility assays | `SnakemakeATACseq` | `sample`, `group`, `replicate`, `fastq_1`, `fastq_2`, `control`, `control_replicate` |
| RNA-seq and related transcriptome assays | `SnakemakeRNAseq` | `sample`, `replicate`, `fastq_1`, `fastq_2`, `strandedness`, `seq_platform` |

Example:

```bash
snakemake \
  --snakefile workflow/Snakefile \
  --config samples=encode_results/snakemake_tf_chip-seq_samplesheet.csv \
  --cores 8
```

## Control strategies

ENCODE can provide more than one control for a case experiment. ENCODEfetch always preserves the full control set in `manifest.tsv`, then uses `--control-strategy` only to decide how exporter samplesheets represent those controls.

Control resolution happens before the strategy is applied:

1. If a case row has file-level `controlled_by_files`, ENCODEfetch maps those control file accessions back to control experiment accessions when possible.
2. If file-level links are not available, ENCODEfetch falls back to `matched_control_experiments`.
3. Duplicate controls are removed while preserving the original ENCODE order.

| Strategy | Behavior |
| --- | --- |
| `all` | Writes one case row per resolved control. A case with two controls appears twice, once for each control. |
| `pool` | Writes one case row and joins all resolved controls in a semicolon-separated value, such as `ENCSRCTRL1;ENCSRCTRL2`. |
| `first` | Writes one case row with the first resolved control. This is deterministic and preserves the original ENCODE/control resolution order. |
| `best` | Writes one case row with the highest-scoring control after metadata ranking. Ties fall back to the original resolved order. |

### Choosing a strategy

Use `all` when the downstream workflow can model multiple controls as separate rows. Use `pool` when the workflow expects one row per case but can receive a pooled control field. Use `first` when you need the previous simple behavior or want exact order-based selection. Use `best` when you want ENCODEfetch to pick the most similar available control.

### Best-control ranking

The `best` strategy scores each candidate control against the case row. Higher scores win. The current ranking rewards:

| Signal | Why it matters |
| --- | --- |
| `biosample_term_id` and `biosample_term_name` | Strongest biological match. |
| `organism` | Prevents cross-organism control selection. |
| `lab` and `award` | Favors controls generated in a similar production context. |
| `classification` | Helps keep cell line, tissue, primary cell, and similar classes aligned. |
| `biological_replicates` and `technical_replicates` | Favors replicate-compatible controls. |
| `run_type`, `paired_end`, and `file_format` | Favors compatible sequencing/file structure. |
| `donor_sex` and `donor_life_stage` | Adds donor-level compatibility when available. |
| released file status and usable file path/URL | Favors controls that are usable by downstream workflows. |

If metadata are missing or all candidates receive the same score, `best` is still deterministic: it returns the first resolved control.

### Examples

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --control-strategy best
```

```python
ef.write_nfcore_sheet(
    df,
    "TF ChIP-seq",
    "nfcore_chipseq.csv",
    control_strategy="first",
)
```

## Python usage

```python
import encodefetch as ef

df, _ = ef.search_accessions(
    ["ENCSR514EOE"],
    file_types={"fastq"},
    status="released",
)
df = ef.collapse_fastq_pairs(df)

ef.write_nfcore_sheet(df, "TF ChIP-seq", "nfcore.csv", control_strategy="best")
ef.write_snakemake_sheet(df, "TF ChIP-seq", "samples.tsv", control_strategy="pool")
```
