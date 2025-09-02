# depois (limpo e funcional)
import re
from sn.api import sn_table_query

GROUP_SYNONYMS = {
    "desktop": "DESKTOP SERVICES",
    "desktop team": "DESKTOP SERVICES",
    "desktop services": "DESKTOP SERVICES",
    "l1 service desk": "L1 SERVICE DESK",
    "service desk": "L1 SERVICE DESK",
    "av": "AV / MEDIA SERVICES",
    "media services": "AV / MEDIA SERVICES",
    "av / media services": "AV / MEDIA SERVICES",
    "ent applications": "ENT APPLICATIONS",
    "enterprise applications": "ENT APPLICATIONS",
    "network": "NETWORK SERVICES",
    "network services": "NETWORK SERVICES",
    "security": "SECURITY - ADMIN",
    "security admin": "SECURITY - ADMIN",
    "security - admin": "SECURITY - ADMIN",
    "security itil": "SECURITY - ITIL Members",
    "security - itil members": "SECURITY - ITIL Members",
    "escalations": "ESCALATIONS",
}

def _extract_group_name(text: str) -> str:
    text_l = text.lower()
    for keyword, official_name in GROUP_SYNONYMS.items():
        if keyword in text_l:
            return official_name
    m = re.search(r"\b([a-z][a-z0-9 _-]+?)\s+team\b", text, flags=re.I)
    if m:
        return m.group(1).strip()
    for phrase in [r"\bservice desk\b", r"\bdesktop\b", r"\bworkplace\b", r"\bit support\b"]:
        if re.search(phrase, text, flags=re.I):
            import re as _re
            return _re.sub(r"\\b", "", phrase).replace("\\", "").strip()
    return ""

def sn_find_group(name_like: str):
    rows = sn_table_query(
        table="sys_user_group",
        query=f"nameLIKE{name_like}",
        fields="sys_id,name",
        limit=1
    )
    if not rows:
        return {"sys_id": None, "name": "none"}
    g = rows[0]
    from sn.utils import _dv
    return {"sys_id": g.get("sys_id"), "name": _dv(g.get("name"))}
