from pathlib import Path
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from nlu.parse import nl_to_filters
from nlu.groups import sn_find_group
from sn.api import sn_table_query, sn_stats_query, sn_find_user
from sn.query_builder import build_incident_query
from agent.system_prompt import SYSTEM_MSG

# Storage (history persisted)
DATA_DIR = Path(__file__).parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = str(DATA_DIR / "agent.db")
storage = SqliteStorage(table_name="agent_sessions", db_file=DB_FILE)

# Agent (same config/behavior)
agent = Agent(
    name="INCIDENT AGENT",
    model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[nl_to_filters, sn_find_group, sn_table_query, sn_stats_query, sn_find_user, build_incident_query],
    debug_mode=True,
    system_message=SYSTEM_MSG,
    storage=storage,
    add_history_to_messages=True,
    num_history_runs=50,
    read_chat_history=True,
    session_id="service_now_chat"
)

# Utility to clear persisted history (optional)

def clear_all_history():
    try:
        db_path = Path(DB_FILE)
        if db_path.exists():
            db_path.unlink()
    except Exception:
        pass
