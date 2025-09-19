from typing import List, Dict, Any
from sn.api import sn_table_query, sn_stats_query
from nlu.groups import resolve_group
from nlu.states import OPEN_STATES
from sn.query_builder import build_incident_query


def open_incidents_by_groups(group_names: List[str], per_group_limit: int = 20) -> Dict[str, Any]:
    """
    Para cada grupo, retorna número de incidentes abertos + alguns exemplos.
    Agora usando assignment_group.display_value em vez de assignment_group (sys_id).
    """
    results = []

    for name in group_names:
        g = resolve_group(name)
        if not g:
            results.append({"group": name, "count": 0, "items": []})
            continue

        # Usamos nome oficial (mais robusto e estável)
        official_name = g["name"]

        filters = {
            "assignment_group.display_value": ("is", official_name),
            "incident_state": ("in", list(OPEN_STATES)),  # já normalizado para códigos
            "active": ("is", "true"),
        }

        query = build_incident_query(
            period="",
            date_field="opened_at",
            filters=filters,
            order_by_desc="sys_updated_on"
        )

        # Contagem total
        stats = sn_stats_query(table="incident", query=query, count=True)
        total_count = int(stats.get("stats", {}).get("count", 0)) if isinstance(stats, dict) else 0

        # Alguns exemplos de incidentes
        items = sn_table_query(
            table="incident",
            query=query,
            fields="number,short_description,caller_id,priority,incident_state,sys_updated_on,assigned_to,assignment_group",
            limit=per_group_limit
        )

        results.append({
            "group": official_name,
            "count": total_count,
            "items": items
        })

    return {"results": results}
