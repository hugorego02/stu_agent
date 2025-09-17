import re
from typing import List, Set, Iterable

# Mapeamento padrão ServiceNow (Incident)
STATE_TO_CODE = {
    "New": "1",
    "In Progress": "2",
    "On Hold": "3",
    "Reopened": "4",
    # 5 (Awaiting Caller) / 8 (Canceled) etc. variam por implementação,
    "Resolved": "6",
    "Closed": "7",
    "Canceled": "8",
}

OPEN_STATES: Set[str] = {"New", "In Progress", "On Hold", "Reopened"}

STATE_SYNONYMS = {
    r"\bopen\b|\bstill open\b": OPEN_STATES,  # "opened" removido (não é estado)
    r"\bnew\b": {"New"},
    r"\bin[\s-]?progress\b": {"In Progress"},
    r"\bon[\s-]?hold\b|\bwaiting\b|\bpending\b": {"On Hold"},
    r"\breopened?\b": {"Reopened"},
    r"\bresolved\b": {"Resolved"},
    r"\bclosed?\b": {"Closed"},
    r"\bcancel(l)?ed\b": {"Canceled"},
}

def _extract_states(text: str) -> List[str]:
    text_l = text.lower()
    found: set = set()
    for pattern, canon in STATE_SYNONYMS.items():
        if re.search(pattern, text_l):
            found |= set(canon)
    return list(found)

def states_to_codes(states: Iterable[str]) -> List[str]:
    codes = []
    for s in states:
        code = STATE_TO_CODE.get(s)
        if code:
            codes.append(code)
    return codes
