import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

SESSION_FILE = DATA_DIR / "session.json"
EMAILS_FILE = DATA_DIR / "emails.json"
BUCKETS_FILE = DATA_DIR / "buckets.json"

DEFAULT_BUCKETS = [
    {
        "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
        "name": "Important",
        "description": "Emails requiring immediate attention or action"
    },
    {
        "id": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e",
        "name": "Can Wait",
        "description": "Emails that can be addressed later without urgency"
    },
    {
        "id": "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f",
        "name": "Auto-archive",
        "description": "Low-priority emails that can be automatically archived"
    },
    {
        "id": "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a",
        "name": "Newsletter",
        "description": "Newsletters, subscriptions, and promotional content"
    }
]


def save_session(token_data: dict) -> None:
    with open(SESSION_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def get_session() -> dict | None:
    if not SESSION_FILE.exists():
        return None
    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def clear_session() -> None:
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def save_emails(emails_data: list[dict]) -> None:
    with open(EMAILS_FILE, "w") as f:
        json.dump(emails_data, f, indent=2)


def get_emails() -> list[dict]:
    if not EMAILS_FILE.exists():
        return []
    with open(EMAILS_FILE, "r") as f:
        return json.load(f)


def save_buckets(buckets: list[dict]) -> None:
    with open(BUCKETS_FILE, "w") as f:
        json.dump(buckets, f, indent=2)


def get_buckets() -> list[dict]:
    if not BUCKETS_FILE.exists():
        save_buckets(DEFAULT_BUCKETS)
        return DEFAULT_BUCKETS
    with open(BUCKETS_FILE, "r") as f:
        return json.load(f)
