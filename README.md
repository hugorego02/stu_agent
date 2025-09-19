ServiceNow Incident Agent

A conversational agent for querying and analyzing ServiceNow incidents in natural language.
Built with Python, it uses Agno Playground, integrates with the ServiceNow API, and can interpret English questions about incidents (counts, listings, group statistics, etc.).

📂 Project Structure
servicenow_agent/
├─ app.py
├─ data/
│  └─ group_cache.json          # ← auto-filled cache for group sys_ids
├─ core/
│  ├─ env.py
│  └─ http.py
├─ sn/
│  ├─ vocab.py
│  ├─ utils.py
│  ├─ dates.py
│  ├─ query_builder.py
│  ├─ api.py
│  └─ reports.py                # ← grouped reports/utilities (e.g., open incidents by group)
├─ nlu/
│  ├─ states.py
│  ├─ groups.py                 # ← hybrid group resolver: FIXED sys_ids + cache + LIKE fallback
│  └─ parse.py
└─ agent/
   ├─ system_prompt.py
   └─ setup.py                  # ← now uses nlu.groups.resolve_group (not sn_find_group)

⚙️ Components
app.py

Entry point of the system.

Starts the Agno Playground web API.

Registers the agent defined in agent/setup.py.

Default port: 7777 (can be changed).

core/
env.py

Loads environment variables from .env:

SN_BASE_URL, SN_USER, SN_PASS, OPENAI_API_KEY, TZ.

Creates HTTP session (requests.Session) with authentication and headers.

Exposes constants:

SN_BASE, SN_USER, SN_PASS, LOCAL_TZ, TIMEOUT, session.

http.py

Core _get(url, params) function for ServiceNow GET calls.

Handles errors and returns data['result'].

sn/ (ServiceNow API & Query Layer)
vocab.py

ServiceNow vocabulary:

REF_FIELDS: reference fields.

KNOWN_FIELDS: supported fields for filters.

OP: maps natural operators (is, contains, between) → ServiceNow operators (=, LIKE, BETWEEN).

_safe(op): ensures only valid operators are used.

utils.py

_dv(value): extracts display_value or "none".

_normalize_refs(row): turns reference fields into human-readable text.

dates.py

Converts natural periods into UTC ranges:

Example: "today", "last week", "this month".

Returns (start_utc, end_utc) and BETWEEN clause.

query_builder.py

Builds sysparm_query string combining filters and periods.

_mk_filter(field, op, value) → incident_stateIN1,2,3,4, caller_idLIKEjohn.

build_incident_query(...) joins all filters with ^.

api.py

ServiceNow API access layer:

sn_table_query(...) → query a table.

sn_stats_query(...) → counts/aggregations.

sn_find_user(...) → resolve user by name.

Uses core.env (session/credentials) + core.http._get.

nlu/ (Natural Language Understanding)
states.py

Maps synonyms like “open”, “in progress”, “on hold” → official ServiceNow states.

_extract_states(text) → returns normalized states.

Converts states into numeric codes used in ServiceNow (1=New, 2=In Progress, 3=On Hold, 4=Reopened).

groups.py

Maps synonyms like “desktop team” → DESKTOP SERVICES.

resolve_group(...) finds official names/sys_ids.

extract_groups(...) supports multiple groups in one query.

parse.py

Main NLU parser.

nl_to_filters(text) converts natural language into filters and period.

Rules:

Defaults to open incidents (incident_state IN {1,2,3,4} AND active=true) if no state mentioned.

Resolves groups, states, people, and dates.

Returns { "period": ..., "filters": {...} }.

agent/
system_prompt.py

System instructions for the agent:

Always reply in English.

Show applied filters in the response.

Limit listings (10–20 items).

Default to open incidents if state not specified.

Use official group names and sys_ids.

Sort results by most recent.

setup.py

Configures the Agno Agent:

Model: OpenAIChat (GPT-based).

Memory: SQLite (data/agent.db) for persistent chat history.

Tools:

nl_to_filters

sn_find_group

sn_table_query

sn_stats_query

sn_find_user

build_incident_query

Can optionally clear all history with clear_all_history().

🔄 Question Flow

User asks a question in Playground (via app.py).

The agent (agent/setup.py) processes it.

nl_to_filters(...) parses the text into structured filters.

If a group is mentioned, sn_find_group(...) resolves the sys_id.

build_incident_query(...) builds the sysparm_query.

Agent executes sn_table_query(...) or sn_stats_query(...).

sn/utils.py normalizes results (display values).

Agent formats the answer according to system_prompt.py.