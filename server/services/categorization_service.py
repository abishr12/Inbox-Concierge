from models.schemas import Bucket, EmailThread
from services.agents.categorization_agent import (
    CategorizationAgentDeps,
    categorization_agent,
)


async def categorize_emails(emails: list[dict], buckets: list[dict]) -> list[dict]:
    # Convert dicts to pydantic models
    email_threads = [EmailThread(**email) for email in emails]
    bucket_models = [Bucket(**bucket) for bucket in buckets]
    
    # Run the categorization agent
    categorization_agent_response = await categorization_agent.run(
        "Categorize the following emails into the appropriate bucket", 
        deps=CategorizationAgentDeps(
            emails=email_threads,
            buckets=bucket_models
        )
    )
    
    print("\n=== Categorization Agent Response ===")
    print(f"Output type: {type(categorization_agent_response.output)}")
    print(f"Output: {categorization_agent_response.output}")
    
    # Map the results back to the email dicts (using .output instead of .data)
    result_map = {result.thread_id: result.bucket_id for result in categorization_agent_response.output}

    # Update the emails with their categories
    categorized_emails = []
    for email in emails:
        email_copy = email.copy()
        email_copy["category"] = result_map.get(email["id"], "")
        categorized_emails.append(email_copy)
    
    return categorized_emails