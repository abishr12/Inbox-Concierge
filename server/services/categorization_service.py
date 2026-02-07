from anthropic import Anthropic
import os
from pydantic_ai import Agent


def categorize_emails(emails: list[dict], buckets: list[str]) -> list[dict]:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    categorized = []
    batch_size = 30
    
    for i in range(0, len(emails), batch_size):
        batch = emails[i:i + batch_size]
        
        prompt = f"""You are an email categorization assistant. Categorize each email into ONE of these buckets: {', '.join(buckets)}

Guidelines:
- Important: Emails requiring action, from known contacts, time-sensitive
- Can Wait: Non-urgent but relevant
- Auto-archive: Automated notifications, receipts
- Newsletter: Marketing, subscriptions, newsletters

Emails to categorize:
{format_emails_for_prompt(batch)}

Return ONLY a JSON array with format: [{{"thread_id": "...", "category": "..."}}]"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        import json
        try:
            categories = json.loads(response_text)
            for item in categories:
                for email in batch:
                    if email["id"] == item["thread_id"]:
                        email["category"] = item["category"]
                        categorized.append(email)
                        break
        except json.JSONDecodeError:
            for email in batch:
                email["category"] = buckets[0]
                categorized.append(email)
    
    return categorized


def format_emails_for_prompt(emails: list[dict]) -> str:
    formatted = []
    for email in emails:
        formatted.append(
            f"ID: {email['id']}\nSubject: {email['subject']}\nFrom: {email['from']}\nSnippet: {email['snippet'][:100]}\n"
        )
    return "\n---\n".join(formatted)
