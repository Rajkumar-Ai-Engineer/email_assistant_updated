"""OAuth for the Gmail and Calendar tools.

Scopes are the minimum the assistant needs. There is no send, delete, or modify
scope for reading, and no tool in this package calls messages.send.
"""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).parents[3]

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",  # drafts only; no tool sends
    "https://www.googleapis.com/auth/calendar.readonly",
]

TOKEN_PATH = Path(os.getenv("GOOGLE_TOKEN_FILE", ROOT / "token.json"))


def _client_secret_path() -> Path:
    env = os.getenv("GOOGLE_CLIENT_SECRET_FILE")
    if env:
        return Path(env)
    matches = sorted(ROOT.glob("client_secret_*.json")) or sorted(
        (ROOT / "credientials").glob("client_secret_*.json")
    )
    if not matches:
        raise FileNotFoundError(
            "No client_secret_*.json in project root or credientials/; "
            "set GOOGLE_CLIENT_SECRET_FILE."
        )
    return matches[0]


def get_credentials() -> Credentials:
    """Load cached credentials, refreshing or running the browser flow if needed."""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(_client_secret_path()), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())
    return creds


def gmail_service():
    return build("gmail", "v1", credentials=get_credentials(), cache_discovery=False)


def calendar_service():
    return build("calendar", "v3", credentials=get_credentials(), cache_discovery=False)
