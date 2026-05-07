import pandas as pd

from encodefetch.exporters.nfcore_chipseq import NFCoreChipseq
from encodefetch.exporters.nfcore_atacseq import NFCoreATACseq
from encodefetch.exporters.nfcore_rnaseq import NFCoreRNAseq
from encodefetch.exporters.snakemake_atacseq import SnakemakeATACseq
from encodefetch.exporters.snakemake_chipseq import SnakemakeChipseq
from encodefetch.exporters.snakemake_rnaseq import SnakemakeRNAseq
from encodefetch.core import write_nfcore_sheet


def _df():
    return pd.DataFrame(
        [
            {
                "experiment_accession": "ENCSRCASE",
                "is_control": False,
                "matched_control_experiments": "ENCSRCTRL1,ENCSRCTRL2",
                "controlled_by_files": "ENCFFCTRL1,ENCFFCTRL2",
                "file_accession": "ENCFFCASE",
                "file_format": "fastq",
                "fastq_1": "case_R1.fastq.gz",
                "fastq_2": "case_R2.fastq.gz",
                "single_end": "false",
                "target_label": "BRD4",
                "biological_replicates": "1",
            },
            {
                "experiment_accession": "ENCSRCTRL1",
                "is_control": True,
                "matched_control_experiments": "",
                "controlled_by_files": "",
                "file_accession": "ENCFFCTRL1",
                "file_format": "fastq",
                "fastq_1": "ctrl1_R1.fastq.gz",
                "fastq_2": "ctrl1_R2.fastq.gz",
                "single_end": "false",
                "target_label": "",
                "biological_replicates": "1",
            },
            {
                "experiment_accession": "ENCSRCTRL2",
                "is_control": True,
                "matched_control_experiments": "",
                "controlled_by_files": "",
                "file_accession": "ENCFFCTRL2",
                "file_format": "fastq",
                "fastq_1": "ctrl2_R1.fastq.gz",
                "fastq_2": "ctrl2_R2.fastq.gz",
                "single_end": "false",
                "target_label": "",
                "biological_replicates": "1",
            },
        ]
    )


def _write_and_read(tmp_path, strategy):
    out = tmp_path / f"{strategy}.csv"
    NFCoreChipseq().write(_df(), out, control_strategy=strategy)
    return pd.read_csv(out).fillna("")


def test_nfcore_control_strategy_all_duplicates_case_rows(tmp_path):
    sheet = _write_and_read(tmp_path, "all")
    case_rows = sheet[sheet["sample"].eq("ENCSRCASE")]

    assert case_rows["control"].tolist() == ["ENCSRCTRL1", "ENCSRCTRL2"]


def test_nfcore_control_strategy_pool_joins_controls(tmp_path):
    sheet = _write_and_read(tmp_path, "pool")
    case_rows = sheet[sheet["sample"].eq("ENCSRCASE")]

    assert case_rows["control"].tolist() == ["ENCSRCTRL1;ENCSRCTRL2"]


def test_nfcore_control_strategy_best_uses_first_control(tmp_path):
    sheet = _write_and_read(tmp_path, "best")
    case_rows = sheet[sheet["sample"].eq("ENCSRCASE")]

    assert case_rows["control"].tolist() == ["ENCSRCTRL1"]


def test_exporters_prefer_local_paths_when_present(tmp_path):
    df = _df()
    df.loc[df["experiment_accession"].eq("ENCSRCASE"), "fastq_1"] = "/tmp/case_R1.fastq.gz"
    df.loc[df["experiment_accession"].eq("ENCSRCASE"), "local_path"] = "/tmp/case_R1.fastq.gz"

    nfcore_out = tmp_path / "nfcore.csv"
    NFCoreChipseq().write(df, nfcore_out)
    nfcore = pd.read_csv(nfcore_out).fillna("")
    assert nfcore[nfcore["sample"].eq("ENCSRCASE")]["fastq_1"].iloc[0] == "/tmp/case_R1.fastq.gz"

    snakemake_out = tmp_path / "snakemake.tsv"
    SnakemakeChipseq().write(df, snakemake_out)
    snakemake = pd.read_csv(snakemake_out, sep="\t").fillna("")
    assert snakemake[snakemake["sample"].eq("ENCSRCASE")]["fastq_1"].iloc[0] == "/tmp/case_R1.fastq.gz"


def test_nfcore_atacseq_matches_required_column_order(tmp_path):
    out = tmp_path / "atacseq.csv"
    NFCoreATACseq().write(_df(), out)
    sheet = pd.read_csv(out).fillna("")

    assert sheet.columns.tolist() == [
        "sample",
        "fastq_1",
        "fastq_2",
        "replicate",
        "control",
        "control_replicate",
    ]
    assert sheet[sheet["sample"].eq("ENCSRCASE")]["control_replicate"].tolist() == [1, 1]


def test_nfcore_rnaseq_matches_required_column_order(tmp_path):
    df = _df()
    df["platform"] = "Illumina NovaSeq 6000"
    out = tmp_path / "rnaseq.csv"
    NFCoreRNAseq().write(df, out)
    sheet = pd.read_csv(out).fillna("")

    assert sheet.columns.tolist() == [
        "sample",
        "fastq_1",
        "fastq_2",
        "strandedness",
        "seq_platform",
    ]
    assert sheet["strandedness"].tolist() == ["auto", "auto", "auto"]
    assert sheet["seq_platform"].tolist() == ["ILLUMINA", "ILLUMINA", "ILLUMINA"]


def test_snakemake_chipseq_preserves_paired_fastqs_and_controls(tmp_path):
    out = tmp_path / "chipseq.tsv"
    SnakemakeChipseq().write(_df(), out, control_strategy="pool")
    sheet = pd.read_csv(out, sep="\t").fillna("")
    case_rows = sheet[sheet["sample"].eq("ENCSRCASE")]

    assert sheet.columns.tolist() == [
        "sample",
        "group",
        "replicate",
        "fastq_1",
        "fastq_2",
        "control",
        "control_replicate",
        "antibody",
    ]
    assert case_rows["fastq_2"].tolist() == ["case_R2.fastq.gz"]
    assert case_rows["control"].tolist() == ["ENCSRCTRL1;ENCSRCTRL2"]


def test_snakemake_atacseq_preserves_paired_fastqs_and_controls(tmp_path):
    out = tmp_path / "atacseq.tsv"
    SnakemakeATACseq().write(_df(), out, control_strategy="best")
    sheet = pd.read_csv(out, sep="\t").fillna("")
    case_rows = sheet[sheet["sample"].eq("ENCSRCASE")]

    assert sheet.columns.tolist() == [
        "sample",
        "group",
        "replicate",
        "fastq_1",
        "fastq_2",
        "control",
        "control_replicate",
    ]
    assert case_rows["fastq_2"].tolist() == ["case_R2.fastq.gz"]
    assert case_rows["control"].tolist() == ["ENCSRCTRL1"]


def test_snakemake_rnaseq_preserves_paired_fastqs_and_strandedness(tmp_path):
    df = _df()
    df["platform"] = "Illumina NovaSeq 6000"
    out = tmp_path / "rnaseq.tsv"
    SnakemakeRNAseq().write(df, out)
    sheet = pd.read_csv(out, sep="\t").fillna("")

    assert sheet.columns.tolist() == [
        "sample",
        "replicate",
        "fastq_1",
        "fastq_2",
        "strandedness",
        "seq_platform",
    ]
    assert sheet[sheet["sample"].eq("ENCSRCASE")]["fastq_2"].tolist() == ["case_R2.fastq.gz"]
    assert sheet["strandedness"].tolist() == ["auto", "auto", "auto"]


def test_nfcore_dispatch_accepts_common_chipseq_and_dnase_spellings(tmp_path):
    chipseq_out = tmp_path / "chipseq.csv"
    dnase_out = tmp_path / "dnase.csv"

    write_nfcore_sheet(_df(), "ChIP-seq", chipseq_out)
    write_nfcore_sheet(_df(), "DNase-seq", dnase_out)

    assert pd.read_csv(chipseq_out).columns.tolist() == [
        "sample",
        "fastq_1",
        "fastq_2",
        "replicate",
        "antibody",
        "control",
        "control_replicate",
    ]
    assert pd.read_csv(dnase_out).columns.tolist() == [
        "sample",
        "fastq_1",
        "fastq_2",
        "replicate",
        "control",
        "control_replicate",
    ]
