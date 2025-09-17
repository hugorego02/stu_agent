import re
from typing import Optional, Dict, Tuple
from sn.api import sn_table_query, sn_find_group
from sn.utils import _dv

# Mapa de sinônimos → nome OFICIAL do grupo
GROUP_SYNONYMS: Dict[str, str] = {
    # Desktop
    "desktop team": "DESKTOP SERVICES",
    "desktop": "DESKTOP SERVICES",
    "desktop services": "DESKTOP SERVICES",
    "workplace": "DESKTOP SERVICES",
    "it support": "DESKTOP SERVICES",

    # Service/Help Desk & Tiers
    "service desk": "L1 SERVICE DESK",
    "help desk": "L1 SERVICE DESK",
    "l1 service desk": "L1 SERVICE DESK",
    "tier 1": "L1 SERVICE DESK",
    "tier1": "L1 SERVICE DESK",
    "tier 2": "TIER 2",
    "tier2": "TIER 2",
    "tier 3": "TIER 3",
    "tier3": "TIER 3",

    # AV / Media
    "av": "AV / MEDIA SERVICES",
    "media services": "AV / MEDIA SERVICES",
    "av / media services": "AV / MEDIA SERVICES",

    # Applications
    "ent applications": "ENT APPLICATIONS",
    "enterprise applications": "ENT APPLICATIONS",
    "applications team": "ENT APPLICATIONS",

    # Network
    "network": "NETWORK SERVICES",
    "network team": "NETWORK SERVICES",
    "network services": "NETWORK SERVICES",

    # Security
    "security": "SECURITY - ADMIN",
    "security admin": "SECURITY - ADMIN",
    "security - admin": "SECURITY - ADMIN",
    "security itil": "SECURITY - ITIL Members",
    "security - itil members": "SECURITY - ITIL Members",

    # Outros
    "escalations": "ESCALATIONS",
    "facilities": "FACILITIES",
}

# Padrões adicionais para frases livres
_TEAM_FALLBACK_PATTERNS = [
    r"\b([a-z][a-z0-9 _-]+?)\s+team\b",   # "X team" → captura X
    r"\bservice desk\b",
    r"\bdesktop\b",
    r"\bworkplace\b",
    r"\bit support\b",
]

def _extract_group_hint(text: str) -> str:
    """Retorna um hint textual (user wording) que será mapeado a um nome oficial."""
    tl = text.lower()

    # 1) Sinônimos diretos
    for k, official in GROUP_SYNONYMS.items():
        if k in tl:
            return official

    # 2) "X team"
    m = re.search(_TEAM_FALLBACK_PATTERNS[0], text, flags=re.I)
    if m:
        # Tentativa de mapear "X team" via sinônimo (ex.: "desktop team" -> DESKTOP SERVICES)
        x = m.group(1).strip().lower()
        candidate = f"{x} team"
        if candidate in GROUP_SYNONYMS:
            return GROUP_SYNONYMS[candidate]
        # Se não houver sinônimo explícito, devolve o termo bruto para tentativa de LIKE
        return x

    # 3) Padrões soltos
    for pat in _TEAM_FALLBACK_PATTERNS[1:]:
        if re.search(pat, text, flags=re.I):
            flat = re.sub(r"\\b", "", pat).replace("\\", "").strip()
            # Se houver sinônimo, usa oficial
            if flat in GROUP_SYNONYMS:
                return GROUP_SYNONYMS[flat]
            return flat

    return ""


def resolve_group(text: str) -> Optional[Dict[str, str]]:
    """
    Resolve um grupo a partir do texto:
    - Aplica sinônimos → nome oficial (preferencial).
    - Busca no ServiceNow por nome EXATO; se não achar, faz LIKE.
    - Retorna {"sys_id": ..., "name": <OFICIAL display_value>}.
    """
    hint = _extract_group_hint(text)
    if not hint:
        return None

    # 1) Tenta exato primeiro
    rows = sn_table_query(
        table="sys_user_group",
        query=f"name={hint}",
        fields="sys_id,name",
        limit=1
    )
    if not rows:
        # 2) Fallback LIKE se veio algo não canônico
        rows = sn_table_query(
            table="sys_user_group",
            query=f"nameLIKE{hint}",
            fields="sys_id,name",
            limit=1
        )
    if not rows:
        return None

    g = rows[0]
    return {"sys_id": g.get("sys_id"), "name": _dv(g.get("name"))}
