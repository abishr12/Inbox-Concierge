from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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
        snippet = message.get("snippet", "")
        
        email_data.append({
            "id": thread["id"],
            "subject": subject,
            "snippet": snippet,
            "from": from_,
            "date": date,
            "category": ""
        })
    
    return email_data
