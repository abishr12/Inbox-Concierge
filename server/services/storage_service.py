import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

SESSION_FILE = DATA_DIR / "session.json"
EMAILS_FILE = DATA_DIR / "emails.json"
BUCKETS_FILE = DATA_DIR / "buckets.json"

DEFAULT_BUCKETS = ["Important", "Can Wait", "Auto-archive", "Newsletter"]


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


def save_buckets(buckets: list[str]) -> None:
    with open(BUCKETS_FILE, "w") as f:
        json.dump(buckets, f, indent=2)


def get_buckets() -> list[str]:
    if not BUCKETS_FILE.exists():
        save_buckets(DEFAULT_BUCKETS)
        return DEFAULT_BUCKETS
    with open(BUCKETS_FILE, "r") as f:
        return json.load(f)
