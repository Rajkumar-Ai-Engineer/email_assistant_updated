# 📬 Email Assistant

An AI-powered email assistant built with LangGraph, DeepAgents, and Gmail/Google Calendar APIs. It reads, triages, searches, drafts replies, and manages your calendar — with a human-in-the-loop approval gate before anything is ever sent.

---

## Features

- **Inbox Reader** — fetches, summarizes, and triages recent emails with priority and category labels
- **Mail Searcher** — searches the full mailbox using Gmail search syntax with evidence-cited answers
- **Calendar Agent** — lists events and finds free slots in your timezone
- **Draft Writer** — writes reply drafts and saves them to Gmail Drafts (never sends automatically)
- **Compose Flow** — multi-turn compose with LangGraph human-in-the-loop send approval
- **Prompt Injection Detection** — flags suspicious email content before the agent acts on it
- **Structured Logging** — JSON structured logs via `structlog` written to timestamped log files
- **Custom Exception Handling** — `EmailCustomException` captures file name and line number from `sys.exc_info()`

---

## Project Structure

```
email_assistant/
├── src/
│   ├── config/
│   │   └── config.yaml              # LLM provider and model config
│   ├── constant/                    # Shared constants
│   ├── core/
│   │   ├── agents/
│   │   │   ├── email_agent.py       # Main orchestrator agent
│   │   │   └── compose_agent.py     # Compose + HITL send agent
│   │   ├── prompts/
│   │   │   └── prompt_factory.py    # All system prompts via PromptContext
│   │   ├── services/
│   │   │   └── mail_service.py      # Service layer (inbox, search, draft, send)
│   │   ├── subagents/
│   │   │   └── mail_subagents.py    # Subagent builder (inbox, search, calendar, draft)
│   │   ├── tools/
│   │   │   ├── gmail_tools.py       # LangChain tools for Gmail + Calendar APIs
│   │   │   └── google_auth.py       # OAuth2 credential management
│   │   └── validators/              # Pydantic schemas for all agent I/O
│   │       ├── common.py
│   │       ├── inbox_reader.py
│   │       ├── mail_searcher.py
│   │       ├── draft_writer.py
│   │       └── calendar_agent.py
│   ├── exception/
│   │   └── custom_exception.py      # EmailCustomException with sys traceback
│   ├── logger/
│   │   └── custom_logger.py         # EmailCustomLogger using structlog + file handler
│   └── utils/
│       ├── config_loader.py         # Safe YAML config loader
│       └── model_loader.py          # LLM model ID loader from config
├── Skills/                          # Agent skill definitions (markdown)
├── app.py                           # Streamlit UI
├── main.py                          # Entry point
├── requirements.txt
├── pyproject.toml
└── .env
```

---

## Architecture

```
Streamlit UI (app.py)
       │
       ▼
  mail_service.py  (service layer)
       │
       ▼
  EmailAgent  ──► DeepAgent (LangGraph)
       │
       ├──► inbox-reader   subagent  ──► get_inbox, get_email, get_thread
       ├──► mail-searcher  subagent  ──► search_emails, get_email
       ├──► calendar-agent subagent  ──► get_calendar, get_free_busy
       └──► draft-writer   subagent  ──► get_email, save_draft

  ComposeAgent  ──► save_draft ──► [HITL interrupt] ──► send_draft
```

All prompts are injected via `PromptContext` (user name, email, timezone, working hours). No prompt contains hardcoded user data.

---

## Prerequisites

- Python 3.11+
- A Google Cloud project with Gmail API and Google Calendar API enabled
- A `client_secret_*.json` OAuth2 credentials file placed in the project root or `credientials/`
- A [Groq](https://console.groq.com) API key

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/email_assistant.git
cd email_assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=<your_groq_api_key>
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=email-assistant
GOOGLE_CLIENT_SECRET_FILE=credientials/client_secret_<...>.json
GOOGLE_TOKEN_FILE=token.json
```

### 4. Configure models

Edit `src/config/config.yaml`:

```yaml
Model:
  llm:
    provider_1:
      model_id: "groq:qwen/qwen3.8-27b"
    provider_2:
      model_id: "groq:openai/gpt-oss-120b"
```

### 5. Authenticate with Google

On first run, a browser window will open for OAuth2 consent. The token is cached in `token.json`.

---

## Running the App

```bash
streamlit run app.py
```

---

## Logging

Logs are written to timestamped JSON files under `logs/`:

```
logs/
└── 05_28_2025_14_32_01.log
```

Each log line is a JSON object:

```json
{"timestamp": "2025-05-28T14:32:01Z", "level": "info", "event": "email_agent_ready"}
```

---

## Exception Handling

All exceptions are wrapped in `EmailCustomException`, which captures the originating file and line number:

```
[src/core/agents/email_agent.py] line 24 — EmailAgent init failed: ...
```

---

## Security

- **No send tool** is exposed to the main agent — only the compose agent has `send_draft`, behind a LangGraph interrupt
- **Human-in-the-loop** — the recipient address must be re-typed to confirm before any draft is sent
- **Prompt injection detection** — email bodies are treated as untrusted data; suspected injections are flagged
- **Least-privilege tool sets** — each subagent only receives the tools it needs
- **Path traversal protection** — log directory and config paths are resolved and validated against the project root

---

## Requirements

```
langchain
langgraph
deepagents
python-dotenv
langchain-groq
ipykernel
streamlit
structlog
pyyaml
pydantic
google-api-python-client
google-auth-oauthlib
```

---

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
