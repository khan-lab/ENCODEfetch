from encodefetch.core import build_file_record, extract_accessions_from_paths


def test_extract_accessions_from_paths_handles_strings_dicts_and_dedupes():
    values = [
        "/files/ENCFF000AAA/",
        "ENCFF000BBB",
        {"accession": "ENCFF000CCC"},
        {"@id": "/files/ENCFF000AAA/"},
        {},
        "",
        None,
    ]

    assert extract_accessions_from_paths(values) == [
        "ENCFF000AAA",
        "ENCFF000BBB",
        "ENCFF000CCC",
    ]


def test_build_file_record_extracts_controlled_by_files():
    exp_json = {
        "accession": "ENCSR000CASE",
        "target": {"label": "BRD4"},
        "biosample_ontology": {"term_name": "K562"},
        "lab": {"title": "Lab"},
        "award": {"rfa": "ENCODE4"},
        "replicates": [{"library": {"biosample": {"donor": {}}}}],
    }
    file_json = {
        "accession": "ENCFF000CASE",
        "file_format": "fastq",
        "status": "released",
        "controlled_by": [
            "/files/ENCFF000CTRL1/",
            {"@id": "/files/ENCFF000CTRL2/"},
        ],
    }

    record = build_file_record(
        file_json,
        exp_json=exp_json,
        is_control=False,
        matched_controls="ENCSR000CTRL",
    )

    assert record["controlled_by_files"] == "ENCFF000CTRL1,ENCFF000CTRL2"
