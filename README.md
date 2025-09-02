Project tree overview
servicenow_agent/
├─ app.py
├─ core/
│  ├─ env.py
│  └─ http.py
├─ sn/
│  ├─ vocab.py
│  ├─ utils.py
│  ├─ dates.py
│  ├─ query_builder.py
│  └─ api.py
├─ nlu/
│  ├─ states.py
│  ├─ groups.py
│  └─ parse.py
└─ agent/
   ├─ system_prompt.py
   └─ setup.py

What each part does
app.py

Entry point of the system.

Starts the Agno Playground web API and registers your agent to chat.

If you want to change the port (default 7777), do it here.

core/
env.py

Loads .env variables (SN_BASE_URL, SN_USER, SN_PASS, OPENAI_API_KEY, TZ).

Creates the HTTP session (requests.Session) with auth and headers.

Exposes constants: SN_BASE, SN_USER, SN_PASS, LOCAL_TZ, TIMEOUT, session.

http.py

Central _get(...) function for ServiceNow HTTP calls.

Handles errors and returns the JSON result.

sn/ (“ServiceNow”—everything that talks directly to the API or builds queries)
vocab.py

ServiceNow vocabulary and operators:

REF_FIELDS, KNOWN_FIELDS (common/allowed fields).

OP (maps “is”, “contains”, “between”, etc.).

_safe(op) ensures a valid operator.

utils.py

Convenience helpers:

_dv(...) gets display_value from reference fields.

_normalize_refs(row) turns references into “pretty” text.

dates.py

Converts natural periods into a UTC range: “today”, “last week”, “this month”…

Returns (start_utc, end_utc) and helps build a BETWEEN clause.

query_builder.py

Builds sysparm_query:

_mk_filter(field, op, value) → stateIN1,2,3, caller_idLIKEjohn, etc.

build_incident_query(period, date_field, filters, order_by_desc) joins everything with ^.

api.py

ServiceNow access layer:

sn_table_query(...) → list records from a table.

sn_stats_query(...) → stats/counts.

sn_find_user(...) → resolve a user by name.

Uses core.env (session/creds) + core.http._get.

nlu/ (“natural language understanding”)
states.py

Rules to detect states (“open/new/in progress/on hold/reopened…”).

_extract_states(text) returns normalized state values.

groups.py

Maps group synonyms (“desktop team” → “DESKTOP SERVICES”).

_extract_group_name(text) tries to find the mentioned team.

sn_find_group(name_like) resolves the group sys_id in ServiceNow.

parse.py

Natural language → search filters:

nl_to_filters(text) returns { period: "", filters: {...} }.

Rule: if the user says “open”, map to open states; if a team is mentioned, resolve assignment_group.

agent/
system_prompt.py

System prompt: agent instructions (reply only in English, how to answer, examples, list limits, etc.).

setup.py

Creates the Agno agent:

Defines the model (OpenAI), memory (SqliteStorage), and the tools the agent can call:
nl_to_filters, sn_find_group, sn_table_query, sn_stats_query, sn_find_user, build_incident_query.

Configures history (turn count, session_id, etc.).

Memory lives in data/agent.db (SQLite) to let the agent remember conversation context.

Question flow (step by step)

The user asks in the Playground (via app.py).

The agent (agent/setup.py) receives the text.

The agent calls nl_to_filters(...) (NLU) to turn the sentence into filters (state, group, etc.).

If there’s a team, sn_find_group(...) resolves the assignment_group sys_id.

build_incident_query(...) builds the sysparm_query (period + filters + ORDERBYDESC).

The agent calls sn_table_query(...) or sn_stats_query(...) (in sn/api.py).

sn/api.py uses core/http.py + core/env.py to make the ServiceNow request.

sn/utils.py normalizes display_values before returning.

The agent formats the response according to the rules in system_prompt.py.