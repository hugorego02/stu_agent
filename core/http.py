from .env import session, TIMEOUT
import requests


def _get(url, params=None, timeout=TIMEOUT):
    try:
        r = session.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        return data.get("result", [])
    except requests.HTTPError as e:
        raise RuntimeError(f"ServiceNow HTTPError: {e.response.status_code} {e.response.text[:200]}") from e
    except Exception as e:
        raise RuntimeError(f"ServiceNow request failed: {e}") from e
