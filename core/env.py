from pathlib import Path
import os
from dotenv import load_dotenv
import requests

# ---------------------------
# Env & Session (unchanged behavior)
# ---------------------------
env_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG OPENAI_API_KEY:", (os.getenv("OPENAI_API_KEY") or "")[:8], "...")
print("DEBUG SN_BASE_URL:", os.getenv("SN_BASE_URL"))

SN_BASE = (os.getenv("SN_BASE_URL") or "").rstrip("/")
SN_USER = os.getenv("SN_USER", "")
SN_PASS = os.getenv("SN_PASS", "")
LOCAL_TZ = os.getenv("TZ", "America/New_York")
TIMEOUT = 45

session = requests.Session()
if SN_USER and SN_PASS:
    session.auth = (SN_USER, SN_PASS)
session.headers.update({"Accept": "application/json"})