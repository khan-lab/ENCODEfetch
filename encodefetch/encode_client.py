from typing import List, Tuple, Optional, Dict, Any
import requests

ENCODE_BASE = "https://www.encodeproject.org"
HEADERS = {"accept": "application/json"}

def encode_get(path_or_url: str,
               params: Optional[list | dict] = None,
               auth=None,
               timeout: int = 120,
               raw_query: Optional[str] = None) -> Dict[str, Any] | None:
    url = path_or_url if path_or_url.startswith("http") else (
        ENCODE_BASE.rstrip("/") + "/" + path_or_url.lstrip("/")
    )
    if params is None:
        params = []
    elif isinstance(params, dict):
        params = list(params.items())
    else:
        params = list(params)

    if not any(k == "format" for k, _ in params):
        params.append(("format", "json"))

    s = requests.Session()
    req = requests.Request("GET", url, headers=HEADERS, params=params, auth=auth)
    prepped = s.prepare_request(req)
    if raw_query:
        sep = '&' if '?' in prepped.url else '?'
        prepped.url = f"{prepped.url}{sep}{raw_query}"
    r = s.send(prepped, timeout=timeout)
    r.raise_for_status()
    return r.json()

def fetch_experiment(accession: str, auth=None, embedded: bool = True):
    params = {"format": "json"}
    if embedded:
        params["frame"] = "embedded"
    return encode_get(f"/experiments/{accession}/", params=params, auth=auth)

def build_params(
    assay_title: Optional[str] = None,
    target_labels: Optional[list[str]] = None,
    organism: Optional[str] = None,
    status: str = "released",
    limit: str = "all",
    extra_params: Optional[dict] = None,
    perturbed: Optional[str] = None,
) -> List[Tuple[str, str]]:
    """Build a list of (key, value) params (repeated keys preserved)."""
    p: List[Tuple[str, str]] = [("type","Experiment")]
    if assay_title:
        p.append(("assay_title", assay_title))
    if status:
        p.append(("status", status))
    if organism:
        p.append(("replicates.library.biosample.donor.organism.scientific_name", organism))
    if perturbed is not None:
        p.append(("perturbed", perturbed.lower()))
    if target_labels:
        for lbl in target_labels:
            for v in str(lbl).split(","):
                v = v.strip()
                if v:
                    p.append(("target.label", v))
    if limit:
        p.append(("limit", limit))
    else:
        p.append(("limit", "all"))
    if extra_params:
        for k, v in extra_params.items():
            p.append((k, str(v)))
    p.append(("format","json"))
    return p
