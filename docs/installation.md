# Installation

## From PyPI

```bash
pip install encodefetch
```

## From source

```bash
git clone https://github.com/khan-lab/ENCODEfetch.git
cd ENCODEfetch
pip install -e .
```

## Requirements

- Python 3.9 or newer.
- Internet access to [encodeproject.org](https://www.encodeproject.org) for live searches and downloads.
- Optional ENCODE authentication token for protected or authenticated requests.

## Development install

```bash
git clone https://github.com/khan-lab/ENCODEfetch.git
cd ENCODEfetch
pip install -e ".[dev,docs]"
pytest
mkdocs build --strict
```

The docs are built with MkDocs from the repository root.
