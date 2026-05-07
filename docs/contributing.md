# Contributing

Contributions are welcome. See the repository-level [CONTRIBUTING.md](https://github.com/khan-lab/ENCODEfetch/blob/main/CONTRIBUTING.md) for the full project guidelines.

## Local setup

```bash
git clone https://github.com/khan-lab/ENCODEfetch.git
cd ENCODEfetch
pip install -e ".[dev,docs]"
pytest
mkdocs build --strict
```

## Good contribution targets

- Add assay-specific normalization in `encodefetch/assays/`.
- Add exporters in `encodefetch/exporters/`.
- Extend metadata fields in `build_file_record`.
- Improve examples and add tests for generated samplesheets.
- Report ENCODE records that need special handling.
