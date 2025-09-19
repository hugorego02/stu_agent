import re
from typing import Optional, Dict
from sn.api import sn_table_query
from sn.utils import _dv

# Cache local para evitar múltiplas chamadas repetidas
_GROUP_CACHE: Dict[str, Dict[str, str]] = {}

# Sinônimos → nome oficial
GROUP_SYNONYMS: Dict[str, str] = {
    "desktop team": "DESKTOP SERVICES",
    "desktop": "DESKTOP SERVICES",
    "desktop services": "DESKTOP SERVICES",
    "workplace": "DESKTOP SERVICES",
    "it support": "DESKTOP SERVICES",

    "service desk": "L1 SERVICE DESK",
    "help desk": "L1 SERVICE DESK",
    "l1 service desk": "L1 SERVICE DESK",
    "tier 1": "L1 SERVICE DESK",
    "tier1": "L1 SERVICE DESK",
    "tier 2": "TIER 2",
    "tier2": "TIER 2",
    "tier 3": "TIER 3",
    "tier3": "TIER 3",

    "av": "AV / MEDIA SERVICES",
    "media services": "AV / MEDIA SERVICES",
    "av / media services": "AV / MEDIA SERVICES",

    "ent applications": "ENT APPLICATIONS",
    "enterprise applications": "ENT APPLICATIONS",
    "applications team": "ENT APPLICATIONS",

    "network": "NETWORK SERVICES",
    "network team": "NETWORK SERVICES",
    "network services": "NETWORK SERVICES",

    "security": "SECURITY - ADMIN",
    "security admin": "SECURITY - ADMIN",
    "security - admin": "SECURITY - ADMIN",
    "security itil": "SECURITY - ITIL Members",
    "security - itil members": "SECURITY - ITIL Members",

    "escalations": "ESCALATIONS",
    "facilities": "FACILITIES",
}

def resolve_group(text: str) -> Optional[Dict[str, str]]:
    """
    Resolve nome → sys_id oficial do grupo.
    Usa cache, sinônimos e fallback LIKE.
    Retorna {"sys_id": ..., "name": <display_value>}
    """
    tl = text.lower().strip()

    # 1) Cache direto
    if tl in _GROUP_CACHE:
        return _GROUP_CACHE[tl]

    # 2) Sinônimos
    official = GROUP_SYNONYMS.get(tl, text)

    # 3) Tenta exato
    rows = sn_table_query(
        table="sys_user_group",
        query=f"name={official}",
        fields="sys_id,name",
        limit=1
    )
    if not rows:
        # 4) Fallback LIKE
        rows = sn_table_query(
            table="sys_user_group",
            query=f"nameLIKE{official}",
            fields="sys_id,name",
            limit=1
        )
    if not rows:
        return None

    g = rows[0]
    resolved = {"sys_id": g.get("sys_id"), "name": _dv(g.get("name"))}

    # Cacheia para próximas vezes
    _GROUP_CACHE[tl] = resolved
    return resolved
