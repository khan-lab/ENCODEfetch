# Examples

These examples are intended to be copied and adjusted for a project. Use `--metadata-only` first to inspect the manifest before downloading large files.

## Find BRD4 TF ChIP-seq FASTQs

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --organism "Homo sapiens" \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --snakemake
```

## Download the same dataset

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --organism "Homo sapiens" \
  --file-type fastq \
  --progress \
  --threads 8 \
  --nfcore \
  --snakemake
```

## Metadata and nf-core samplesheet only

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --file-type fastq \
  --metadata-only \
  --nfcore \
  --control-strategy best
```

## Accessions mode

```bash
encodefetch \
  --accessions ENCSR514EOE,ENCSR395MHA \
  --file-type fastq \
  --metadata-only \
  --progress
```

## Accessions file mode

```bash
encodefetch \
  --accessions accessions.txt \
  --file-type fastq \
  --metadata-only \
  --nfcore
```

## Human unperturbed multi-target search

```bash
encodefetch \
  --assay-title "TF ChIP-seq" \
  --target-label BRD4 \
  --target-label SMAD3 \
  --organism "Homo sapiens" \
  --perturbed false \
  --file-type fastq \
  --metadata-only
```

## Related ENCODE series type

```bash
encodefetch \
  --assay-title "RNA-seq" \
  --series OrganismDevelopmentSeries \
  --file-type fastq \
  --metadata-only \
  --progress
```

## Python exporter smoke test

```python
import pandas as pd
from encodefetch.exporters.nfcore_chipseq import NFCoreChipseq

df = pd.DataFrame(
    [
        {
            "experiment_accession": "ENCSRCASE",
            "is_control": False,
            "matched_control_experiments": "ENCSRCTRL",
            "controlled_by_files": "ENCFFCTRL",
            "file_accession": "ENCFFCASE",
            "file_format": "fastq",
            "fastq_1": "case_R1.fastq.gz",
            "fastq_2": "case_R2.fastq.gz",
            "target_label": "BRD4",
            "biological_replicates": "1",
        },
        {
            "experiment_accession": "ENCSRCTRL",
            "is_control": True,
            "file_accession": "ENCFFCTRL",
            "file_format": "fastq",
            "fastq_1": "ctrl_R1.fastq.gz",
            "fastq_2": "ctrl_R2.fastq.gz",
            "biological_replicates": "1",
        },
    ]
)

NFCoreChipseq().write(df, "nfcore_chipseq.csv", control_strategy="all")
```
