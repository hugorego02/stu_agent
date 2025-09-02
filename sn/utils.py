from typing import Dict, Any
from .vocab import REF_FIELDS


def _dv(value: Any) -> str:
    if isinstance(value, dict):
        dv = value.get("display_value")
        if dv is None or (isinstance(dv, str) and not dv.strip()):
            return "none"
        return str(dv)
    if isinstance(value, str) and value.strip():
        return value
    return "none"


def _normalize_refs(row: Dict[str, Any]) -> Dict[str, Any]:
    for f in list(row.keys()):
        if f in REF_FIELDS:
            row[f] = _dv(row[f])
    return row