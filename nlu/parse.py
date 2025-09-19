import re
from typing import Dict, Tuple, Any

from .states import _extract_states, OPEN_STATES, states_to_codes
from .groups import resolve_group

def nl_to_filters(text: str):
    filters: Dict[str, Tuple[str, Any]] = {}

    # 1) Estado
    states = _extract_states(text)
    if states:
        codes = states_to_codes(states)
        if codes:
            filters["incident_state"] = ("in", codes)
    else:
        codes = states_to_codes(list(OPEN_STATES))
        filters["incident_state"] = ("in", codes)
        filters["active"] = ("is", "true")

    # 2) Grupo
    grp = resolve_group(text)
    if grp and grp.get("sys_id"):
        filters["assignment_group"] = ("is", grp["sys_id"])

    return {"period": "", "filters": filters}
