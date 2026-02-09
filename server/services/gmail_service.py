import html
import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def clean_snippet(snippet: str) -> str:
    """Clean email snippet by removing HTML entities and invisible unicode characters."""
    # Decode HTML entities (e.g., &#39; -> ')
    snippet = html.unescape(snippet)
    
    # Remove invisible/zero-width unicode characters commonly used in email marketing
    invisible_chars = [
        '\u034f',  # Combining grapheme joiner
        '\u200b',  # Zero-width space
        '\u200c',  # Zero-width non-joiner
        '\u200d',  # Zero-width joiner
        '\u2060',  # Word joiner
        '\ufeff',  # Zero-width no-break space
        '\u00a0',  # Non-breaking space (replace with regular space)
        '\u2019',  # Apostrophe
    ]
    
    for char in invisible_chars:
        if char == '\u00a0':
            snippet = snippet.replace(char, ' ')
        elif char == '\u2019':
            snippet = snippet.replace(char, "'")
        else:
            snippet = snippet.replace(char, '')
    
    # Remove excessive whitespace
    snippet = re.sub(r'\s+', ' ', snippet).strip()
    
    return snippet


def get_last_threads(credentials_dict: dict, num_threads: int) -> list[dict]:
    credentials = Credentials(**credentials_dict)
    service = build("gmail", "v1", credentials=credentials)
    
    results = service.users().threads().list(userId="me", maxResults=num_threads).execute()
    threads = results.get("threads", [])
    
    email_data = []
    for thread in threads:
        thread_detail = (
            service.users().threads().get(userId="me", id=thread["id"]).execute()
        )
        messages = thread_detail.get("messages", [])
        if not messages:
            continue
        
        message = messages[0]
        headers = message.get("payload", {}).get("headers", [])
        
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        from_ = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "")
        snippet = clean_snippet(message.get("snippet", ""))
        
        email_data.append({
            "id": thread["id"],
            "subject": subject,
            "snippet": snippet,
            "from": from_,
            "date": date,
            "label_id": "",
            "label_name": ""
        })
    
    return email_data
