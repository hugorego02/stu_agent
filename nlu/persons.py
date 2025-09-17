# nlu/persons.py
import re
from typing import Optional, Tuple
from sn.api import sn_find_user

ROLE_TO_FIELD = {
    "requested for": "requested_for",
    "requester": "requested_for",
    "student": "requested_for",
    "caller": "caller_id",
    "user": "caller_id",
    "from": "caller_id",
}

ROLE_PAT = re.compile(r"\b(requested\s*for|requester|student|caller|user|from)\b\s*([a-z][a-z .'-]+)", re.I)
NAME_ONLY_PAT = re.compile(r"\bfor\s+([a-z][a-z .'-]+)\b", re.I)

def extract_person_filter(text: str) -> Optional[Tuple[str, str]]:
    m = ROLE_PAT.search(text)
    if m:
        role = m.group(1).lower()
        name = m.group(2).strip()
        field = ROLE_TO_FIELD.get(role, "caller_id")
        u = sn_find_user(name)
        return (field, u["sys_id"] if u.get("sys_id") else name)

    m2 = NAME_ONLY_PAT.search(text)
    if m2:
        name = m2.group(1).strip()
        field = "requested_for"
        u = sn_find_user(name)
        return (field, u["sys_id"] if u.get("sys_id") else name)
    return None
