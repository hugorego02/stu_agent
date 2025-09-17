from typing import Any

# Campos de referência (mostrar display_value)
REF_FIELDS = {
    "caller_id", "assignment_group", "assigned_to", "category", "subcategory",
    "cmdb_ci", "parent", "parent_incident", "problem_id", "company",
    # trocado: remover u_service/u_service_offering e usar os oficiais
    "service", "service_offering",
    "origin", "opened_by", "closed_by",
    "location", "requested_for", "request", "change_request"
}

# Campos conhecidos (podemos passar qualquer um, mas isto guia validações/heurísticas)
KNOWN_FIELDS = {
    "number", "short_description", "description",
    # datas
    "opened_at", "sys_created_on", "sys_updated_on", "resolved_at", "closed_at",
    # status
    "incident_state", "state", "active",
    # prioridade/impacto/etc.
    "priority", "impact", "urgency", "severity",
    # categorização
    "category", "subcategory",
    # relacionamentos / ref
    "assignment_group", "assigned_to", "caller_id", "requested_for",
    "location", "company", "service", "service_offering", "parent_incident",
    # contadores / SLA
    "reassignment_count", "reopen_count", "made_sla", "sla_due",
    # novos: criador/fechador
    "sys_created_by", "closed_by"
}

OP = {
    "is": "=",
    "is not": "!=",
    "is one of": "IN",
    "is not one of": "NOT IN",
    "is empty": "ISEMPTY",
    "is not empty": "ISNOTEMPTY",
    "less than": "<",
    "greater than": ">",
    "less than or is": "<=",
    "greater than or is": ">=",
    "between": "BETWEEN",
    "is anything": "ANYTHING",
    "is same": "SAMEAS",
    "is different": "NSAMEAS",
    "is empty string": "ISEMPTYSTRING",
    "contains": "LIKE",
    "not contains": "NOT LIKE",
    "starts with": "STARTSWITH",
    "ends with": "ENDSWITH"
}

def _safe(op: str) -> str:
    return OP.get(op.strip().lower(), "=")
