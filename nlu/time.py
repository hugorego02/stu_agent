import re
from datetime import datetime, timedelta
import pytz

SUPPORTED_PERIODS = {
    "today","yesterday","this week","last week","this month","last month",
    "last 7 days","last 30 days","last 60 days","last 90 days","last 120 days",
    "last 12 months","this quarter","last quarter","this year","last year","last hour"
}

def detect_date_field(text: str) -> str:
    t = text.lower()
    if "resolved" in t: 
        return "resolved_at"
    if "closed" in t: 
        return "closed_at"
    if "updated" in t: 
        return "sys_updated_on"
    if "created" in t or "came in" in t: 
        return "sys_created_on"
    return "opened_at"

def detect_period_or_filters(text: str, local_tz: str = "America/New_York"):
    """
    Retorna (period, extra_filters_marker)
    - period: um dos SUPPORTED_PERIODS (ou "")
    - extra_filters_marker: {"__between__": (startUTC, endUTC)} ou {"__lt__": cutoffUTC} quando aplicável
    """
    tl = text.lower()
    extra = {}

    # business hours de hoje (08:00–18:00)
    if "business hours" in tl or "business hour" in tl:
        tz = pytz.timezone(local_tz)
        now = datetime.now(tz)
        start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        end = now.replace(hour=18, minute=0, second=0, microsecond=0)
        extra["__between__"] = (
            start.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
            end.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
        )
        return ("", extra)

    # último fim de semana (sábado-domingo recente)
    if "weekend" in tl:
        tz = pytz.timezone(local_tz)
        now = datetime.now(tz)
        days_back = (now.weekday() - 5) % 7  # 5 = sábado (0=seg)
        sat = (now - timedelta(days=days_back)).replace(hour=0, minute=0, second=0, microsecond=0)
        sun = sat + timedelta(days=1, hours=23, minutes=59, seconds=59)
        extra["__between__"] = (
            sat.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
            sun.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
        )
        return ("", extra)

    # older than N days
    m = re.search(r"older than (\d+)\s+days", tl)
    if m:
        n = int(m.group(1))
        tz = pytz.timezone(local_tz)
        cutoff = datetime.now(tz) - timedelta(days=n)
        extra["__lt__"] = cutoff.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        return ("", extra)

    for p in SUPPORTED_PERIODS:
        if p in tl:
            return (p, extra)

    if "today" in tl:
        return ("today", extra)

    return ("", extra)
