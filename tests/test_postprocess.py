import pandas as pd

from encodefetch.postprocess import collapse_fastq_pairs


def test_collapse_fastq_pairs_keeps_r2_accession_from_indexed_mate():
    df = pd.DataFrame(
        [
            {
                "experiment_accession": "ENCSRCASE",
                "is_control": False,
                "file_accession": "ENCFFR1",
                "file_format": "fastq",
                "run_type": "paired-ended",
                "paired_end": "1",
                "paired_accession": "ENCFFR2",
                "file_status": "released",
                "url": "https://example.org/ENCFFR1.fastq.gz",
                "md5sum": "md5-r1",
                "file_size": 1,
                "biological_replicates": "1",
                "technical_replicates": "1_1",
            },
            {
                "experiment_accession": "ENCSRCASE",
                "is_control": False,
                "file_accession": "ENCFFR2",
                "file_format": "fastq",
                "run_type": "paired-ended",
                "paired_end": "2",
                "paired_accession": "ENCFFR1",
                "file_status": "released",
                "url": "https://example.org/ENCFFR2.fastq.gz",
                "md5sum": "md5-r2",
                "file_size": 2,
                "biological_replicates": "1",
                "technical_replicates": "1_1",
            },
        ]
    )

    collapsed = collapse_fastq_pairs(df)

    assert collapsed["file_accession"].tolist() == ["ENCFFR1"]
    assert collapsed["file_accession_r2"].tolist() == ["ENCFFR2"]
