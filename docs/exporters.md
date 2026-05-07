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

ENCODE can provide more than one control. ENCODEfetch preserves all controls in `manifest.tsv`, then lets you choose how samplesheets represent them:

| Strategy | Behavior |
| --- | --- |
| `all` | Duplicates the case row once per control. |
| `pool` | Writes all controls in a single semicolon-separated value. |
| `best` | Uses the first control deterministically. |

File-level `controlled_by` links are preferred when present. If they are absent, exporter control columns fall back to experiment-level `matched_control_experiments`.

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
