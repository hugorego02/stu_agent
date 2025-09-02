from typing import Dict, List, Tuple, Any
from .vocab import _safe
from .dates import _utc_range, _between_clause


def _mk_filter(field: str, operator: str, value: Any) -> str:
    field = field.strip()
    op = _safe(operator)
    if op in ("ISEMPTY", "ISNOTEMPTY", "ANYTHING"):
        return f"{field}{op}"
    if op == "ISEMPTYSTRING":
        return f"{field}={''}"
    if op in ("IN", "NOT IN") and isinstance(value, (list, tuple, set)):
        joined = ",".join(str(v) for v in value if str(v).strip())
        return f"{field}{op}{joined}"
    if op in ("LIKE", "NOT LIKE", "STARTSWITH", "ENDSWITH"):
        return f"{field}{op}{value}"
    return f"{field}{op}{value}"


def build_incident_query(
    period: str = "",
    date_field: str = "opened_at",
    filters: Dict[str, Tuple[str, Any]] = None,
    order_by_desc: str = "sys_updated_on"
) -> str:
    parts: List[str] = []
    if period:
        s, e = _utc_range(period)
        parts.append(_between_clause(date_field, s, e))
    if filters:
        for f, (op, val) in filters.items():
            parts.append(_mk_filter(f, op, val))
    if order_by_desc:
        parts.append(f"ORDERBYDESC{order_by_desc}")
    return "^".join(parts)