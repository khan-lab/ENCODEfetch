# Interactive API (Notebook-friendly)

Use a single call that **returns a DataFrame only** (does not write files):

```python
from encodefetch.interactive import fetch_dataframe

df = fetch_dataframe(
  assay_title="TF ChIP-seq",
  target_labels=["BRD4","SMAD3"],
  organism="Homo sapiens",
  file_types={"fastq"},
  status="released",
  progress=True,
  threads=8,
  collapse_fastqs=True,
)
df.head()
```

## Function source

```python
from __future__ import annotations
from typing import Optional, List, Set, Tuple
import pandas as pd
from encodefetch.core import search_experiments as _search_experiments
from encodefetch.core import search_accessions as _search_accessions
from encodefetch.postprocess import collapse_fastq_pairs

def fetch_dataframe(
    *,
    accessions: Optional[List[str]] = None,
    assay_title: Optional[str] = None,
    target_labels: Optional[List[str]] = None,
    organism: Optional[str] = None,
    file_types: Optional[Set[str]] = None,
    assembly: Optional[str] = None,
    status: str = "released",
    perturbed: Optional[str] = None,
    progress: bool = False,
    threads: int = 6,
    collapse_fastqs: bool = True,
    auth_token: Optional[str] = None,
) -> pd.DataFrame:
    """Interactive-friendly DataFrame fetcher."""
    if accessions:
        df, _ = _search_accessions(
            accessions,
            file_types=file_types,
            assembly=assembly,
            status=status,
            auth_token=auth_token,
            progress=progress,
            threads=threads,
        )
    else:
        df, _ = _search_experiments(
            assay_title=assay_title,
            target_labels=target_labels,
            organism=organism,
            file_types=file_types,
            assembly=assembly,
            status=status,
            auth_token=auth_token,
            progress=progress,
            perturbed=perturbed,
            threads=threads,
        )
    if df.empty:
        return df
    return collapse_fastq_pairs(df) if collapse_fastqs else df
```
