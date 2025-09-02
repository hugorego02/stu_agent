from typing import Any

REF_FIELDS = {
    "caller_id", "assignment_group", "assigned_to", "category", "subcategory",
    "cmdb_ci", "parent", "parent_incident", "problem_id", "company",
    "u_service", "u_service_offering", "u_origin", "opened_by", "closed_by",
    "location", "requested_for", "request", "change_request"
}

KNOWN_FIELDS = {
    "number", "short_description", "description",
    "opened_at", "sys_created_on", "sys_updated_on", "resolved_at", "closed_at",
    "incident_state", "state", "active", "priority", "impact", "urgency", "severity",
    "category", "subcategory", "assignment_group", "assigned_to", "caller_id",
    "reassignment_count", "reopen_count", "made_sla", "sla_due",
    "location", "company", "u_service", "u_service_offering", "parent_incident"
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