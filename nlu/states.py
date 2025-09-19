import re
from typing import List, Dict, Set

# -------------------------
# Oficial states (nome + código)
# -------------------------
STATE_MAP: Dict[str, Dict] = {
    "New": {"code": "1", "aliases": ["new", "just opened"]},
    "In Progress": {"code": "2", "aliases": ["in progress", "working", "active work"]},
    "On Hold": {"code": "3", "aliases": ["on hold", "waiting", "pending"]},
    "Reopened": {"code": "4", "aliases": ["reopen", "reopened", "again"]},
    "Resolved": {"code": "6", "aliases": ["resolved", "fixed", "done", "completed"]},
    "Closed": {"code": "7", "aliases": ["closed", "finished", "terminated"]},
    "Canceled": {"code": "8", "aliases": ["canceled", "cancelled", "aborted"]},
}

OPEN_STATES: Set[str] = {"New", "In Progress", "On Hold", "Reopened"}

# Estados resolvidos/fechados/cancelados
RESOLVED_STATES: Set[str] = {"Resolved", "Closed", "Canceled"}

# -------------------------
# Utils
# -------------------------
def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _extract_states(text: str) -> List[str]:
    """
    Retorna nomes oficiais de estados encontrados no texto.
    Ex: "show resolved incidents" → ["Resolved"]
    """
    tl = _normalize_text(text)
    found: List[str] = []

    for official, data in STATE_MAP.items():
        # Match no nome oficial
        if official.lower() in tl:
            found.append(official)
            continue

        # Match nos aliases
        for alias in data["aliases"]:
            if alias in tl:
                found.append(official)
                break

    return list(set(found))  # remove duplicatas


def states_to_codes(states: List[str]) -> List[str]:
    """
    Converte nomes oficiais de estados em códigos numéricos.
    Ex: ["Resolved", "Closed"] → ["6", "7"]
    """
    codes: List[str] = []
    for st in states:
        if st in STATE_MAP:
            codes.append(STATE_MAP[st]["code"])
    return codes
