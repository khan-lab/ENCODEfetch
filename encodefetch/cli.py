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

click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True

@click.command(help="ENCODEfetch: a command-line tool for retrieving matched case-control data and standardized metadata from ENCODE.\n\n"
                    "Author: Aziz Khan <aziz.khan@mbzuai.ac.ae>\n"
                    "https://github.com/khan-lab/ENCODEfetch")

@click.option("--accessions", default=None, help="Comma-separated experiment accessions.")
@click.option("--assay-title", default="Histone ChIP-seq", show_default=True, help="Assay title.")
@click.option("--target-label", multiple=True, help="Target label(s); repeat or comma-separate.")
@click.option("--organism", default=None, help="Organism scientific name.")
@click.option("--file-type", "file_type", multiple=True,
              type=click.Choice(["fastq","bam","bed","bigWig","tsv","bw","bedpe"], case_sensitive=False),
              help="File formats to include.")
@click.option("--assembly", default=None, help="Assembly filter.")
@click.option("--status", default="released", show_default=True, help="File status filter.")
@click.option("--perturbed", type=click.Choice(["true","false"], case_sensitive=False),
              default=None, help="Filter experiments by 'perturbed'.")
@click.option("--outdir", default="encode_results", show_default=True, 
              help="Output directory.")
@click.option("--download", is_flag=True, default=False, 
              help="Download files.")

@click.option("--threads", default=6, show_default=True, 
              help="Workers for downloads.")

@click.option("--max-retries", default=3, show_default=True, type=int,
              help="Max HTTP retries per file during download.")
@click.option("--chunk-size", default=1024*1024, show_default=True, type=int,
              help="Download chunk size in bytes (e.g., 1048576 for 1 MiB).")

@click.option("--dry-run", is_flag=True, default=False, 
              help="Only write manifest/metadata; skip downloads.")
@click.option("--auth-token", default=None, 
              help="ENCODE API token.")
@click.option("--progress/--no-progress", default=True, 
              help="Show progress bars.")
@click.option("--nfcore", is_flag=True, default=False, 
              help="Write nf-core chipseq samplesheet.")
@click.option("--snakemake", is_flag=True, default=False, 
              help="Write Snakemake samplesheet.")

# The main function
def main(accessions, 
         assay_title, 
         target_label, 
         organism, 
         file_type, 
         assembly, 
         status,
         perturbed, 
         outdir, 
         download, 
         threads, 
         dry_run, 
         auth_token, 
         progress, 
         nfcore, 
         snakemake, 
         max_retries, 
         chunk_size
         ):
    
    file_types = set([ft.lower() for ft in file_type]) if file_type else None
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)

    if accessions:
        acc_list = [a.strip() for a in accessions.split(",") if a.strip()]
        df, records = search_accessions(acc_list, file_types=file_types, assembly=assembly, status=status,
                                       auth_token=auth_token, progress=progress)
    else:
        df, records = search_experiments(assay_title=assay_title,
                                         target_labels=list(target_label) if target_label else None,
                                         organism=organism,
                                         file_types=file_types,
                                         assembly=assembly,
                                         status=status,
                                         auth_token=auth_token,
                                         progress=progress,
                                         perturbed=perturbed)

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

    if download and not dry_run:
        files_dir = outdir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        def make_dest(row):
            typ = "control" if row.is_control else "case"
            exp = row.experiment_accession
            acc = row.file_accession
            fmt = (row.file_format or "dat").lower()
            return files_dir / typ / exp / f"{acc}.{fmt}"

        # Build tasks from dataframe (skip if already present)
        items = []
        for row in df.itertuples(index=False):
            dest = make_dest(row)
            if dest.exists():
                continue
            size = int(row.file_size) if str(row.file_size).isdigit() else None
            label = f"{row.file_accession} ({row.experiment_accession})"
            items.append({
                "url": row.url,
                "dest": dest,
                "size": size,
                "label": label
            })

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
                        chunk=chunk_size, retries=max_retries
                    ))

                # Wait for all; exceptions will surface here
                for fut in futures:
                    fut.result()

        # Update manifest with local_path
        local_paths = []
        for _, row in df.iterrows():
            typ = "control" if row["is_control"] else "case"
            exp = row["experiment_accession"]
            acc = row["file_accession"]
            fmt = (row["file_format"] or "dat").lower()
            path = files_dir / typ / exp / f"{acc}.{fmt}"
            local_paths.append(str(path) if path.exists() else "")
        df["local_path"] = local_paths
        df.to_csv(outdir / "manifest.tsv", sep="\t", index=False)
        click.echo(f"Updated manifest with local paths: {outdir / 'manifest.tsv'}")


    if nfcore:
        write_nfcore_sheet(df, outdir / "nfcore_chipseq_samplesheet.csv")
        click.echo(f"NF-core sample sheet: {outdir / 'nfcore_chipseq_samplesheet.csv'}")
    if snakemake:
        write_snakemake_sheet(df, outdir / "snakemake_samples.tsv")
        click.echo(f"Snakemake sample sheet: {outdir / 'snakemake_samples.tsv'}")
