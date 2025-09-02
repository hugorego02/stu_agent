import re
from typing import Dict, Tuple, Any
from .states import _extract_states
from .groups import _extract_group_name, sn_find_group


def nl_to_filters(text: str):
    """
    Parse a user sentence and return inferred period and filters.
    Returns: {"period": str|"", "filters": { field: (op, value) }}
    Rules remain identical to the original implementation.
    """
    filters: Dict[str, Tuple[str, Any]] = {}

    states = _extract_states(text)
    if states:
        filters["state"] = ("is one of", states)
    else:
        if re.search(r"\bopen\b|\bstill open\b", text, flags=re.I):
            filters["active"] = ("is", "true")

    group_guess = _extract_group_name(text)
    if group_guess:
        g = sn_find_group(group_guess)
        if g.get("sys_id"):
            filters["assignment_group"] = ("is", g["sys_id"])
        else:
            filters["assignment_group"] = ("is", group_guess.title())

    period = ""
    return {"period": period, "filters": filters}