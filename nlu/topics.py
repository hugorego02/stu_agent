from typing import Dict, Tuple, Any
import re

TOPIC_MAP: Dict[str, Dict[str, Tuple[str, Any]]] = {
    "password reset": {"subcategory": ("is", "password reset")},
    "network": {"category": ("is", "network")},
    "email": {"category": ("is", "email")},
    "vpn": {"short_description": ("contains", "vpn")},
    "printer": {"category": ("is", "hardware"), "short_description": ("contains", "printer")},
    "wi-fi": {"short_description": ("contains", "wi-fi")},
    "wifi": {"short_description": ("contains", "wifi")},
    "software installation": {"subcategory": ("contains", "install")},
    "hardware": {"category": ("is", "hardware")},
    "servicenow": {"short_description": ("contains", "servicenow")},
    "urgent": {"urgency": ("is", "1")},
    "critical": {"priority": ("is", "1")},
    "p1": {"priority": ("is", "1")},
    "p2": {"priority": ("is", "2")},
    "medium priority": {"priority": ("is", "3")},
    "low priority": {"priority": ("is", "4")},
}

def extract_topic_filters(text: str) -> Dict[str, Tuple[str, Any]]:
    filters: Dict[str, Tuple[str, Any]] = {}
    tl = text.lower()
    for key, fmap in TOPIC_MAP.items():
        if key in tl:
            filters.update(fmap)
    # fallback genérico p/ "tickets about X"
    m = re.search(r"\b(issues?|tickets?) (about|related to) ([a-z0-9 \-_/]+)", tl)
    if m and "short_description" not in filters:
        filters["short_description"] = ("contains", m.group(3).strip())
    return filters
