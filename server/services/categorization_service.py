from models.schemas import Bucket, EmailThread
from services.agents.categorization_agent import (
    CategorizationAgentDeps,
    categorization_agent,
)


async def categorize_emails(
    emails: list[dict], buckets: list[dict]
) -> list[dict]:
    """Categorize a list of emails against the given buckets via a single LLM call.

    Callers are responsible for batching — this function processes
    whatever list it receives in one pass.
    """
    bucket_models = [Bucket(**bucket) for bucket in buckets]
    email_threads = [EmailThread(**email) for email in emails]

    categorization_agent_response = await categorization_agent.run(
        "Categorize the following emails into the appropriate bucket",
        deps=CategorizationAgentDeps(emails=email_threads, buckets=bucket_models),
    )

    # Map the results back
    result_map = {
        result.thread_id: {
            "bucket_id": result.bucket_id,
            "bucket_name": result.bucket_name,
        }
        for result in categorization_agent_response.output
    }

    # Update emails with categories
    categorized = []
    for email in emails:
        email_copy = email.copy()
        label = result_map.get(email["id"], {})
        email_copy.update(
            {
                "label_id": label.get("bucket_id", ""),
                "label_name": label.get("bucket_name", ""),
            }
        )
        categorized.append(email_copy)

    return categorized
