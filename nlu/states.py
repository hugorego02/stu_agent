import re
from typing import List, Set

OPEN_STATES: Set[str] = {"New", "In Progress", "On Hold", "Reopened"}
STATE_SYNONYMS = {
    r"\bopen\b|\bstill open\b|\bopened\b": OPEN_STATES,
    r"\bnew\b": {"New"},
    r"\bin[\s-]?progress\b": {"In Progress"},
    r"\bon[\s-]?hold\b|\bwaiting\b|\bpending\b": {"On Hold"},
    r"\breopened?\b": {"Reopened"},
    r"\bresolved\b": {"Resolved"},
    r"\bclosed?\b": {"Closed"},
}


def _extract_states(text: str) -> List[str]:
    text_l = text.lower()
    found: set = set()
    for pattern, canon in STATE_SYNONYMS.items():
        if re.search(pattern, text_l):
            found |= set(canon)
    return list(found)