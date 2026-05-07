# Quickstart

## Metadata-first ChIP-seq run

Start with `--metadata-only` while exploring filters. This avoids large downloads and still writes the manifest plus samplesheets.

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --organism "Homo sapiens" \
  --file-type fastq \
  --status released \
  --metadata-only \
  --nfcore \
  --snakemake \
  --outdir encode_results
```

ENCODEfetch will:

1. Search ENCODE for released human BRD4 TF ChIP-seq experiments.
2. Fetch each experiment and expand matched controls.
3. Keep case and control file records together.
4. Collapse paired FASTQs into `fastq_1` and `fastq_2`.
5. Write `manifest.tsv`, `metadata.jsonl`, and optional samplesheets.

## Download files

Remove `--metadata-only` to download matching files into `encode_results/files/`.

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --organism "Homo sapiens" \
  --file-type fastq \
  --status released \
  --progress \
  --threads 8
```

## Fetch known accessions

```bash
encodefetch \
  --accessions ENCSR514EOE,ENCSR395MHA \
  --file-type fastq \
  --metadata-only \
  --nfcore
```

You can also pass a text file with one accession per line. Blank lines and lines starting with `#` are ignored.

```bash
encodefetch \
  --accessions accessions.txt \
  --file-type fastq \
  --metadata-only \
  --nfcore
```

## Use Python

```python
import encodefetch as ef

df, records = ef.search_experiments(
    assay_title="TF ChIP-seq",
    target_labels=["BRD4"],
    organism="Homo sapiens",
    file_types={"fastq"},
    status="released",
    progress=False,
    threads=4,
)

df = ef.collapse_fastq_pairs(df)
ef.write_nfcore_sheet(df, "TF ChIP-seq", "nfcore_tf_chipseq_samplesheet.csv")
ef.write_snakemake_sheet(df, "TF ChIP-seq", "snakemake_tf_chipseq_samplesheet.csv")
```
