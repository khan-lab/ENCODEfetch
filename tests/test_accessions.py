from encodefetch.cli import parse_accessions_input


def test_parse_accessions_from_string():
    accessions, source = parse_accessions_input("ENCSR000AAA, ENCSR000BBB,,")

    assert source == "string"
    assert accessions == ["ENCSR000AAA", "ENCSR000BBB"]


def test_parse_accessions_from_file(tmp_path):
    path = tmp_path / "accessions.txt"
    path.write_text(
        "\n"
        "# comment\n"
        "   # indented comment\n"
        "ENCSR000AAA\n"
        "ENCSR000BBB\n"
    )

    accessions, source = parse_accessions_input(str(path))

    assert source == "file"
    assert accessions == ["ENCSR000AAA", "ENCSR000BBB"]
