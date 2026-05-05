# ENCODEfetch <img src="docs/img/logo.png" align="right" width="190"/>

[![PyPI](https://img.shields.io/pypi/v/encodefetch.svg?style=flat-square)](https://pypi.org/project/encodefetch/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**ENCODEfetch** is a command-line tool and Python package for retrieving matched case–control datasets and standardized metadata from the [ENCODE Project](https://www.encodeproject.org).

ENCODEfetch automates:

- **Search** for ENCODE experiments by assay, target, organism, status, and more
- **Get case-control matched** experiments
- **File retrieval** (FASTQ, BAM, BED, bigWig, etc.) with filtering by status/assembly
- **Parallel downloads** files with resumable transfers and interactive progress bars.
- **Standardized metadata outputs** (`manifest.tsv`, `metadata.jsonl`).
- **Plug-and-play samplesheets** for [nf-core](https://nf-co.re/) and Snakemake workflows for reproduciable analysis.
- **Interactive API** returning tidy `pandas.DataFrame` objects of metadata with file paths for downstream analysis.

![cli](/docs/img/ENCODEfetch-cli.png)

## 🚀 Installation

### From PyPI (recommended)

```bash
pip install encodefetch
```

### From source

```bash
git clone https://github.com/khan-lab/ENCODEfetch.git
cd ENCODEfetch
pip install -e .
```

Requires **Python 3.9+**. or newer versions.

## 🔧 Command-line usage

```bash
encodefetch --assay-title "TF ChIP-seq" \
             --target-label BRD4,SMAD3 \
             --organism "Homo sapiens" \
             --file-type fastq \
             --status released \
             --progress \
             --threads 8 \
             --nfcore
```

### Key options

- `--accessions ENCSR123ABC,ENCSR456DEF` — fetch experiments by accession directly.
- `--accessions accessions.txt` — read one experiment accession per line; blank lines and `#` comments are ignored.
- `--assay-title` — e.g. `TF ChIP-seq`, `Histone ChIP-seq`, `ATAC-seq`, `RNA-seq`.
- `--target-label` — one or more targets (comma-separated).
- `--organism` — e.g. `Homo sapiens`, `Mus musculus`.
- `--file-type` — restrict formats (`fastq`, `bam`, `bed`, `bigWig`…).
- `--status` — default `released` (can also include `archived`).
- `--perturbed true|false` — filter perturbed experiments.
- `--series OrganismDevelopmentSeries` — filter experiments by related ENCODE series `@type`.
- `--metadata-only` — skip file downloads and write metadata/sample sheets only.
- `--threads` — number of worker threads for metadata fetching, control fetching, and downloads.
- `--max-retries` / `--chunk-size` — tune download retry count and streamed chunk size.
- `--nfcore` / `--snakemake` — export pipeline-ready sample sheets.
- `--control-strategy all|pool|best` — choose how samplesheets represent multiple controls.

Run `encodefetch --help` to see all options.

## 📦 Outputs

After a run, `outdir/` contains:

- **`manifest.tsv`** — tidy table of case/control files with metadata.
- **`metadata.jsonl`** — raw record dump (one JSON per line).
- **`files/`** — downloaded files, organized by experiment/control.
- **`nfcore_*_samplesheet.csv`** — optional nf-core samplesheet.
- **`snakemake_samples.tsv`** — optional Snakemake sample table.

ENCODEfetch preserves all experiment-level controls in `matched_control_experiments`. File-level `controlled_by` links are normalized into `controlled_by_files` when ENCODE provides them. Samplesheets prefer file-level control mappings, then fall back to experiment-level controls; `--control-strategy all` duplicates case rows per control, `pool` joins controls with semicolons, and `best` currently chooses the first control deterministically.

## 🐍 Python API

```python
import encodefetch as ef

# Search experiments
metadata, recs = ef.search_experiments(
    assay_title="TF ChIP-seq",
    target_labels=["BRD4","SMAD3"],
    organism="Homo sapiens",
    series="OrganismDevelopmentSeries",
    file_types={"fastq"},
    status="released",
    progress=False,
    threads=2,
)

metadata.head()

# Collapse paired-end FASTQs to one row
metadata_collapse = ef.collapse_fastq_pairs(metadata)

# Write nf-core samplesheet
ef.write_nfcore_sheet(metadata_collapse, "nfcore_chipseq.csv")

```

## 🧬 Assay support

ENCODEfetch currently provides assay-aware normalization and exporters to nf-core/snakemake samplesheets for:

- **ChIP-seq** (production)
- **ATAC-seq** (in beta)
- **RNA-seq** (in beta)
- more to be added ..

Each assay can plug in its own normalization (e.g., FASTQ collapsing, strandedness detection) and samplesheet exporters.

## 🤝 Contributing

Contributions are welcome!

- Add new **assay classes** under `encodefetch/assays/`.
- Add new **exporters** under `encodefetch/exporters/`.
- Extend metadata fields in `build_file_record`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
