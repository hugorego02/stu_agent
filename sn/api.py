from typing import Any
from .utils import _normalize_refs
from .query_builder import build_incident_query  # re-export (optional usage)
from .vocab import KNOWN_FIELDS, REF_FIELDS
from core.env import SN_BASE, SN_USER, SN_PASS
from core.http import _get

def sn_table_query(
    table: str,
    query: str,
    fields: str = "",
    limit: int = 20,
    offset: int = 0,
    display_value: str = "all"
):
    assert SN_BASE and SN_USER and SN_PASS, "Missing SN_* config"
    url = f"{SN_BASE}/api/now/table/{table}"
    params = {
        "sysparm_query": query,
        "sysparm_limit": max(1, min(int(limit), 100)),
        "sysparm_offset": max(0, int(offset)),
        "sysparm_display_value": display_value
    }
    if fields:
        params["sysparm_fields"] = fields
    rows = _get(url, params)
    return [_normalize_refs(r) for r in rows]

def sn_stats_query(
    table: str,
    query: str = "",
    group_by: str = "",
    having: str = "",
    count: bool = True
):
    assert SN_BASE and SN_USER and SN_PASS, "Missing SN_* config"
    url = f"{SN_BASE}/api/now/stats/{table}"
    params = {}
    if query:
        params["sysparm_query"] = query
    if count:
        params["sysparm_count"] = "true"
    if group_by:
        params["sysparm_group_by"] = group_by
    if having:
        params["sysparm_having"] = having
    return _get(url, params)

def sn_find_user(name_like: str):
    rows = sn_table_query(
        table="sys_user",
        query=f"nameLIKE{name_like}",
        fields="sys_id,name,user_name,email",
        limit=1
    )
    if not rows:
        return {"sys_id": None, "name": "none"}
    u = rows[0]
    from .utils import _dv
    return {"sys_id": u.get("sys_id"), "name": _dv(u.get("name"))}

# --- Melhorado: tenta nome EXATO primeiro; se não achar, usa LIKE ---
def sn_find_group(name_like: str):
    # 1) exato
    rows = sn_table_query(
        table="sys_user_group",
        query=f"name={name_like}",
        fields="sys_id,name",
        limit=1
    )
    if rows:
        g = rows[0]
        from .utils import _dv
        return {"sys_id": g.get("sys_id"), "name": _dv(g.get("name"))}

    # 2) like
    rows = sn_table_query(
        table="sys_user_group",
        query=f"nameLIKE{name_like}",
        fields="sys_id,name",
        limit=1
    )
    if not rows:
        return {"sys_id": None, "name": "none"}
    g = rows[0]
    from .utils import _dv
    return {"sys_id": g.get("sys_id"), "name": _dv(g.get("name"))}
