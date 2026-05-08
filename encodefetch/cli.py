import json
from pathlib import Path
import concurrent.futures as cf

import rich_click as click
from rich.progress import Progress

from .core import (
    search_experiments,
    search_accessions,
    collapse_fastq_pairs,
    download_file,
    write_nfcore_sheet,
    write_snakemake_sheet,
)

from . import __version__

click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True


click.rich_click.OPTION_GROUPS = {
    "encodefetch": [
        {
            "name": "Input selection",
            "options": ["--accessions"],
        },
        {
            "name": "Search filters",
            "options": [
                "--assay-title", "--target-label", "--organism", "--biosample",
                "--perturbed", "--series", "--status"
            ],
        },
        {
            "name": "File filters",
            "options": ["--file-type", "--assembly"],
        },
        {
            "name": "Output options",
            "options": ["--outdir", "--nfcore", "--snakemake", "--control-strategy"],
        },
        {
            "name": "Download options",
            "options": ["--metadata-only", "--max-retries", "--chunk-size"],
        },
        {
            "name": "Performance & UX",
            "options": ["--threads", "--progress"],
        },
        {
            "name": "Miscellaneous",
            "options": ["--dry-run", "--auth-token", "--version", "--help"],
        },
    ]
}

def parse_accessions_input(accessions: str) -> tuple[list[str], str]:
    """Parse accession IDs from a comma-separated string or a text file path."""
    path = Path(accessions)
    if path.is_file():
        parsed = []
        with path.open() as fh:
            for line in fh:
                value = line.strip()
                if not value or value.startswith("#"):
                    continue
                parsed.append(value)
        return parsed, "file"
    parsed = [a.strip() for a in accessions.split(",") if a.strip()]
    return parsed, "string"


@click.command(name="encodefetch", help="ENCODEfetch: a command-line tool for retrieving matched case-control data and standardized metadata from ENCODE.\n\n"
                    "Author: Aziz Khan <aziz.khan@mbzuai.ac.ae>\n"
                    "https://github.com/khan-lab/ENCODEfetch")

@click.option("--accessions", default=None, 
              help="Comma-separated experiment accessions, or a text file with one accession per line.")

@click.option("--assay-title", default="Histone ChIP-seq", 
              show_default=True, help="Assay title.")

@click.option("--target-label", multiple=True, 
              help="Target label(s); repeat or comma-separate.")

@click.option("--organism", default=None, 
              help="Organism scientific name. (e.g. 'Homo sapiens', 'Mus musculus')")

@click.option("--biosample", default=None, 
              help="Biosample ontology term name.")


@click.option("--file-type", "file_type", multiple=True,
              type=click.Choice(["fastq","bam","bed","bigWig","tsv","bw","bedpe"], case_sensitive=False),
              help="File formats to include.")

@click.option("--assembly", default=None, 
              help="Assembly filter.")

@click.option("--status", default="released", show_default=True, 
              help="File status filter.")

@click.option("--perturbed", type=click.Choice(["true","false"], case_sensitive=False),
              default=None, help="Filter experiments by 'perturbed'.")

@click.option("--series", default=None,
              help="Filter experiments by related series @type, e.g. OrganismDevelopmentSeries.")

@click.option("--outdir", default="encode_results", show_default=True, 
              help="Output directory.")

@click.option("--metadata-only", is_flag=True, default=False,
              help="Write manifest/metadata and samplesheets only; skip file downloads.")

@click.option("--threads", default=6, show_default=True, 
              help="Workers for metadata fetching, control fetching, and downloads.")

@click.option("--max-retries", default=3, show_default=True, type=int,
              help="Max HTTP retries per file during download.")

@click.option("--chunk-size", default=5*1024*1024, show_default=True, type=int,
              help="Download chunk size in bytes (e.g., 1048576 for 1 MiB).")

@click.option("--dry-run", is_flag=True, default=False, 
              help="Deprecated alias for --metadata-only.")

@click.option("--auth-token", default=None, 
              help="ENCODE API token.")

@click.option("--progress/--no-progress", default=True, 
              help="Show progress bars.")

@click.option("--nfcore", is_flag=True, default=False, 
              help="Write nf-core chipseq samplesheet.")

@click.option("--snakemake", is_flag=True, default=False, 
              help="Write Snakemake samplesheet.")

@click.option("--control-strategy",
              type=click.Choice(["all", "pool", "best", "first"], case_sensitive=False),
              default="all",
              show_default=True,
              help="Samplesheet strategy for multiple controls.")

@click.version_option(version=__version__, prog_name="ENCODEfetch",
                      message="%(prog)s, version %(version)s")

# The main function
def main(accessions, 
         assay_title, 
         target_label, 
         organism,
         biosample, 
         file_type, 
         assembly, 
         status,
         perturbed, 
         series,
         outdir, 
         metadata_only,
         threads, 
         dry_run, 
         auth_token, 
         progress, 
         nfcore, 
         snakemake, 
         control_strategy,
         max_retries, 
         chunk_size
         ):
    
    file_types = set([ft.lower() for ft in file_type]) if file_type else None
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)

    
    if accessions:
        acc_list, accession_source = parse_accessions_input(accessions)
        source_label = f"file: {accessions}" if accession_source == "file" else "string"
        click.echo(f"Parsed {len(acc_list)} accession(s) from {source_label}.")

        df, records = search_accessions(
            acc_list,
            file_types=file_types,
            assembly=assembly,
            status=status,
            auth_token=auth_token,
            progress=progress,
            threads=threads,
        )

    else:
        df, records = search_experiments(assay_title=assay_title,
                                         target_labels=list(target_label) if target_label else None,
                                         organism=organism,
                                         biosample=biosample,
                                         file_types=file_types,
                                         assembly=assembly,
                                         status=status,
                                         auth_token=auth_token,
                                         progress=progress,
                                         perturbed=perturbed,
                                         series=series,
                                         threads=threads)

    if df.empty:
        click.echo("No files matched your filters.", err=True); return

    if "file_format" in df.columns and df["file_format"].astype(str).str.lower().eq("fastq").any():
        df = collapse_fastq_pairs(df)

    manifest_tsv = outdir / "manifest.tsv"
    meta_jsonl = outdir / "metadata.jsonl"
    df.to_csv(manifest_tsv, sep="\t", index=False)
    with open(meta_jsonl, "w") as f:
        for row in records:
            f.write(json.dumps(row) + "\n")
    click.echo(f"Wrote manifest: {manifest_tsv}")
    click.echo(f"Wrote metadata: {meta_jsonl}")

    def write_samplesheets():
        if nfcore:
            samplesheet_name = f"nfcore_{assay_title.strip().lower().replace(' ', '_')}_samplesheet.csv"
            write_nfcore_sheet(df, assay_title, f"{outdir}/{samplesheet_name}", control_strategy=control_strategy)
            click.echo(f"nf-core sample sheet: {outdir}/{samplesheet_name}")

        if snakemake:
            samplesheet_name = f"snakemake_{assay_title.strip().lower().replace(' ','_')}_samplesheet.csv"
            write_snakemake_sheet(df, assay_title, f"{outdir}/{samplesheet_name}", control_strategy=control_strategy)
            click.echo(f"Snakemake sample sheet: {outdir}/{samplesheet_name}")

    skip_downloads = metadata_only or dry_run

    ## Download files by default unless metadata-only mode is requested.
    if not skip_downloads:
        files_dir = outdir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        def file_ext(file_format):
            fmt = (file_format or "dat").lower()
            if fmt == "fastq":
                fmt = "fastq.gz"
            return fmt

        def make_dest(is_control, experiment_accession, file_accession, file_format):
            typ = "control" if is_control else "case"
            return files_dir / typ / experiment_accession / f"{file_accession}.{file_ext(file_format)}"

        def accession_from_download_url(url):
            value = str(url or "").strip()
            if "/files/" in value:
                return value.split("/files/", 1)[1].strip("/").split("/")[0]
            name = Path(value).name
            return name.split(".", 1)[0] if name else ""

        def parse_file_size(value):
            if value in (None, ""):
                return None
            try:
                size = int(float(value))
            except (TypeError, ValueError):
                return None
            return size if size > 0 else None

        def add_download_item(items, seen, *, url, dest, size, label):
            if not url or not dest or dest in seen or dest.exists():
                return
            seen.add(dest)
            items.append({
                "url": url,
                "dest": dest,
                "size": size,
                "label": label,
            })

        # Build tasks from dataframe (skip if already present)
        items = []
        seen_dests = set()
        for _, row in df.iterrows():
            dest = make_dest(
                row["is_control"],
                row["experiment_accession"],
                row["file_accession"],
                row["file_format"],
            )
            size = parse_file_size(row.get("file_size", ""))
            label = f"{row['file_accession']} ({row['experiment_accession']})"
            add_download_item(items, seen_dests, url=row.get("url", ""), dest=dest, size=size, label=label)

            r2_acc = str(row.get("file_accession_r2", "") or "").strip()
            r2_url = str(row.get("url_r2", "") or "").strip()
            if not r2_acc:
                r2_acc = accession_from_download_url(r2_url)
            if r2_acc and r2_url:
                r2_dest = make_dest(
                    row["is_control"],
                    row["experiment_accession"],
                    r2_acc,
                    row["file_format"],
                )
                r2_size = parse_file_size(row.get("file_size_r2", ""))
                r2_label = f"{r2_acc} ({row['experiment_accession']})"
                add_download_item(items, seen_dests, url=r2_url, dest=r2_dest, size=r2_size, label=r2_label)

        if not items:
            click.echo("All files already present. Skipping downloads.")
        else:
            # Nice rich progress with filename + bytes + speed + ETA
            from rich.progress import (
                Progress, SpinnerColumn, TextColumn, BarColumn,
                DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
            )
            columns = [
                SpinnerColumn(),
                TextColumn("[green]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ]

            with Progress(*columns) as prog, cf.ThreadPoolExecutor(max_workers=threads) as ex:
                futures = []
                for it in items:
                    # One task per file, total = file size if known
                    task_id = prog.add_task(f"Downloading {it['label']}", total=it["size"])
                    futures.append(ex.submit(
                        download_file,
                        it["url"], it["dest"],
                        progress=prog, task_id=task_id,
                        auth=(auth_token, "") if auth_token else None,
                        chunk=chunk_size, retries=max_retries
                    ))

                # Wait for all; exceptions will surface here
                for fut in futures:
                    fut.result()

        # Update manifest and FASTQ columns with local paths.
        local_paths = []
        local_paths_r2 = []
        for _, row in df.iterrows():
            path = make_dest(
                row["is_control"],
                row["experiment_accession"],
                row["file_accession"],
                row["file_format"],
            )
            local_paths.append(str(path) if path.exists() else "")

            r2_acc = str(row.get("file_accession_r2", "") or "").strip()
            if not r2_acc:
                r2_acc = accession_from_download_url(row.get("url_r2", ""))
            if r2_acc:
                path_r2 = make_dest(
                    row["is_control"],
                    row["experiment_accession"],
                    r2_acc,
                    row["file_format"],
                )
                local_paths_r2.append(str(path_r2) if path_r2.exists() else "")
            else:
                local_paths_r2.append("")

        df["local_path"] = local_paths
        if "file_accession_r2" in df.columns:
            df["local_path_r2"] = local_paths_r2
        if "fastq_1" in df.columns:
            df["fastq_1"] = df.apply(lambda r: r["local_path"] or r.get("fastq_1", ""), axis=1)
        if "fastq_2" in df.columns and "local_path_r2" in df.columns:
            df["fastq_2"] = df.apply(lambda r: r["local_path_r2"] or r.get("fastq_2", ""), axis=1)
        df.to_csv(outdir / "manifest.tsv", sep="\t", index=False)
        click.echo(f"Updated manifest with local paths: {outdir / 'manifest.tsv'}")

    write_samplesheets()
