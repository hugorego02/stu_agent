import re
from typing import Dict, Tuple, Any

from .states import _extract_states, OPEN_STATES, states_to_codes
from .groups import resolve_group

# As dependências abaixo são opcionais.
try:
    from .persons import extract_person_filter  # requested_for / caller_id
except Exception:
    def extract_person_filter(_: str):
        return None

try:
    from .time import detect_period_or_filters, detect_date_field
except Exception:
    def detect_period_or_filters(_: str):
        return "", {}
    def detect_date_field(_: str):
        return "opened_at"

try:
    from .topics import extract_topic_filters
except Exception:
    def extract_topic_filters(_: str):
        return {}


def nl_to_filters(text: str):
    """
    Parse user sentence and return inferred period/date_field/filters.

    Regras:
    - Se o usuário NÃO especificar estado, default para "open incidents":
        incident_state IN {1,2,3,4}  (New, In Progress, On Hold, Reopened)  +  active=true
    - Se o usuário especificar estado, respeitar (converter nomes -> códigos).
    - Grupo: resolve para sys_id oficial (resolve_group).
    - Pessoas: requested_for/caller_id (se módulo persons estiver ativo).
    - Período: sem filtro por padrão (salvo detecção explícita).
    """
    filters: Dict[str, Tuple[str, Any]] = {}

    # 1) Estado
    states = _extract_states(text)
    if states:
        codes = states_to_codes(states)
        if codes:
            filters["incident_state"] = ("is one of", codes)
    else:
        # Default: sempre "open incidents"
        codes = states_to_codes(list(OPEN_STATES))  # ["1","2","3","4"]
        filters["incident_state"] = ("is one of", codes)
        filters["active"] = ("is", "true")

    # 2) Pessoa (requested_for / caller_id) - opcional
    pf = extract_person_filter(text)
    if pf:
        field, value = pf
        filters[field] = ("is", value)

    # 3) Grupo (sys_id via resolve_group)
    grp = resolve_group(text)
    if grp and grp.get("sys_id"):
        filters["assignment_group"] = ("is", grp["sys_id"])

    # 4) Tópicos (categoria/priority) - opcional
    topic_filters = extract_topic_filters(text)
    filters.update(topic_filters)

    # 5) Não atribuídos (heurística comum)
    if re.search(r"\bunassigned\b|\bnot assigned\b|\bwaiting for assignment\b", text, flags=re.I):
        filters["assigned_to"] = ("is empty", "")

    # 6) Período e campo de data (opcional)
    date_field = detect_date_field(text)
    period, extras = detect_period_or_filters(text)

    if "__between__" in extras:
        start_utc, end_utc = extras["__between__"]
        filters[date_field] = ("between", f"{start_utc}@{end_utc}")
    if "__lt__" in extras:
        cutoff = extras["__lt__"]
        filters[date_field] = ("less than", cutoff)

    # Mantém o contrato original (period + filters)
    return {"period": period, "filters": filters}
