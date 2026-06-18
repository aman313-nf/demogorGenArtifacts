"""Client for the public Nightfall playground detection API (no auth).

Endpoint + the full callable detector set live in detectors.json. Stdlib-only
(urllib) so it adds no deps and can run inside the Streamlit app or at gen time.
Invalid detector values 500 the endpoint, so we validate against the config and
only ever send known values.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

_CFG = json.loads((Path(__file__).resolve().parent / "detectors.json").read_text())
ENDPOINT = _CFG["endpoint"]
DETECTORS = _CFG["detectors"]                       # [{value,label,ui,category?,description?}]
VALID = {d["value"] for d in DETECTORS}
DATA_TYPE_MAP = _CFG["data_type_map"]               # data_type -> detector value | None
MIN_CONFIDENCE = _CFG["min_confidence_levels"]


def detector_for(data_type: str) -> str | None:
    """Most-relevant detector for one of our generated data types, or None
    ('detector not integrated')."""
    return DATA_TYPE_MAP.get((data_type or "").strip().lower())


def label_for(value: str) -> str:
    for d in DETECTORS:
        if d["value"] == value:
            return d.get("label", value)
    return value


class ScanError(RuntimeError):
    pass


def scan(text: str, detectors: list[str], min_confidence: str = "POSSIBLE",
         timeout: int = 30) -> list[dict]:
    """POST to the playground /scan. Returns a list of findings:
    {detector_name, finding, confidence, start_index, end_index}. Drops any
    detector value not in the config (would 500). Raises ScanError on network
    failure."""
    dets = [d for d in dict.fromkeys(detectors) if d in VALID]   # de-dupe + validate
    if not text.strip() or not dets:
        return []
    body = json.dumps({"text": text, "selectedDetectors": dets,
                       "minConfidence": min_confidence}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise ScanError(str(exc)) from exc
    out = []
    for f in data if isinstance(data, list) else []:
        out.append({
            "detector_name": f.get("detector_name"),
            "finding": f.get("finding", ""),
            "confidence": str(f.get("confidence", "")).split(".")[-1],   # Confidence.X -> X
            "start_index": f.get("start_index"), "end_index": f.get("end_index"),
        })
    return out
