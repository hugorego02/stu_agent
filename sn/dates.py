from datetime import datetime, timedelta
import pytz
import re
from typing import Tuple
from core.env import LOCAL_TZ


def _utc_range(keyword: str) -> Tuple[str, str]:
    tz = pytz.timezone(LOCAL_TZ)
    now = datetime.now(tz)
    k = keyword.strip().lower()

    def to_utc(dt: datetime) -> str:
        return dt.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")

    if k in ("today",):
        start = now.replace(hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("yesterday",):
        d = now - timedelta(days=1)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end = d.replace(hour=23, minute=59, second=59, microsecond=0)
    elif k in ("this week",):
        wd = now.weekday()
        start = (now - timedelta(days=wd)).replace(hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("last week",):
        wd = now.weekday()
        last_mon = (now - timedelta(days=wd + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
        last_sun = last_mon + timedelta(days=6, hours=23, minutes=59, seconds=59)
        start, end = last_mon, last_sun
    elif k in ("this month",):
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("last month",):
        first_this = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = first_this - timedelta(seconds=1)
        start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0); end = last_month_end
    elif re.match(r"last \d+ days", k):
        n = int(re.findall(r"\d+", k)[0]); start = now - timedelta(days=n); end = now
    elif re.match(r"last \d+ months", k):
        n = int(re.findall(r"\d+", k)[0]); start = now - timedelta(days=30*n); end = now
    elif k in ("last 12 months",):
        start = now - timedelta(days=365); end = now
    elif k in ("this quarter",):
        q = (now.month - 1) // 3; first_month = 1 + 3*q
        start = now.replace(month=first_month, day=1, hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("last quarter",):
        q = (now.month - 1) // 3; first_month_this_q = 1 + 3*q
        first_this_q = now.replace(month=first_month_this_q, day=1, hour=0, minute=0, second=0, microsecond=0)
        last_q_end = first_this_q - timedelta(seconds=1)
        q_start_month = ((first_month_this_q - 3 - 1) % 12) + 1
        q_start_year = last_q_end.year if q_start_month <= last_q_end.month else last_q_end.year - 1
        start = last_q_end.replace(year=q_start_year, month=q_start_month, day=1, hour=0, minute=0, second=0, microsecond=0); end = last_q_end
    elif k in ("this year",):
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("last year",):
        start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(year=now.year - 1, month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
    elif k in ("last 2 years",):
        start = now.replace(year=now.year - 2, month=1, day=1, hour=0, minute=0, second=0, microsecond=0); end = now
    elif k in ("current hour",):
        start = now.replace(minute=0, second=0, microsecond=0); end = now
    elif k in ("last hour",):
        end = now.replace(minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        start = end - timedelta(hours=1) + timedelta(seconds=1)
    elif re.match(r"last (\d+ )?minutes", k) or k in ("current minute",):
        if k == "current minute":
            start = now.replace(second=0, microsecond=0); end = now
        else:
            import re as _re
            n = int(_re.findall(r"\d+", k)[0]) if _re.findall(r"\d+", k) else 1
            start = now - timedelta(minutes=n); end = now
    else:
        raise ValueError(f"Unsupported period: '{keyword}'")

    def _between_clause(field: str, start_utc: str, end_utc: str) -> str:
        return f"{field}BETWEEN{start_utc}@{end_utc}"

    return to_utc(start), to_utc(end)


def _between_clause(field: str, start_utc: str, end_utc: str) -> str:
    return f"{field}BETWEEN{start_utc}@{end_utc}"