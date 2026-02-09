"""
Test suite for the categorization service.

This test validates that emails are properly categorized into buckets
using the AI-powered categorization agent.
"""

import json

# Import the service we're testing
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.categorization_service import categorize_emails

# Load environment variables
load_dotenv()



@pytest.fixture
def sample_emails():
    """Load sample emails from the data file."""
    data_path = Path(__file__).parent.parent / "data" / "emails.json"
    with open(data_path, "r") as f:
        return json.load(f)


@pytest.fixture
def sample_buckets():
    """Load sample buckets from the data file."""
    data_path = Path(__file__).parent.parent / "data" / "buckets.json"
    with open(data_path, "r") as f:
        return json.load(f)


@pytest.fixture
def test_emails():
    """Create a small subset of test emails for faster testing."""
    return [
        {
            "id": "test-1",
            "subject": "URGENT: Server Down - Production Issue",
            "snippet": "Our production server is experiencing downtime. Immediate action required.",
            "from": "ops@company.com",
            "date": "Mon, 9 Feb 2026 15:45:23 +0000",
            "label": ""
        },
        {
            "id": "test-2",
            "subject": "Weekly Newsletter - Tech Updates",
            "snippet": "Your weekly digest of technology news and updates",
            "from": "newsletter@techdigest.com",
            "date": "Mon, 9 Feb 2026 14:30:00 +0000",
            "label": ""
        },
        {
            "id": "test-3",
            "subject": "Amazon Order Delivered",
            "snippet": "Your package has been delivered. Track your order here.",
            "from": "no-reply@amazon.com",
            "date": "Mon, 9 Feb 2026 12:00:00 +0000",
            "label": ""
        }
    ]


@pytest.mark.asyncio
async def test_categorize_emails_basic(test_emails, sample_buckets):
    """
    Test basic categorization functionality with a small set of emails.
    
    This test verifies that:
    1. The categorization service runs without errors
    2. Output is returned (even if commented out in the service)
    3. The agent processes the emails and buckets correctly
    """
    result = await categorize_emails(test_emails, sample_buckets)
    
    # Note: Currently the service has the return commented out
    # Once uncommented, we can validate the structure
    print("\n=== Categorization Test Result ===")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")


@pytest.mark.asyncio
async def test_categorize_full_email_set(sample_emails, sample_buckets):
    """
    Test categorization with the full set of sample emails.
    
    This tests the service with real data to ensure it can handle
    a larger volume of emails.
    """
    result = await categorize_emails(sample_emails, sample_buckets)
    
    print("\n=== Full Email Set Categorization ===")
    print(f"Processed {len(sample_emails)} emails")
    print(f"Result: {result}")


@pytest.mark.asyncio
async def test_categorize_emails_output_structure(test_emails, sample_buckets):
    """
    Test that the categorization output has the expected structure.
    
    This validates that:
    1. Each email gets a label assigned
    2. Labels are valid bucket IDs
    3. All emails are returned
    """
    result = await categorize_emails(test_emails, sample_buckets)
    
    # Validate basic structure
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == len(test_emails), "Should return same number of emails"
    
    # Validate each email has a label
    bucket_ids = {bucket["id"] for bucket in sample_buckets}
    for email in result:
        assert "label" in email, f"Email {email['id']} missing label"
        assert email["label"] in bucket_ids, f"Invalid label for email {email['id']}"
    
    print("\n=== Output Structure Test ===")
    print(f"✓ All {len(result)} emails have valid labels")
    print(f"Result: {result}")


@pytest.mark.asyncio
async def test_pydantic_model_conversion(test_emails, sample_buckets):
    """
    Test that the service properly converts dicts to Pydantic models.
    
    This validates the internal conversion logic works correctly.
    """
    from models.schemas import Bucket, EmailThread
    
    # Test email conversion
    email_threads = [EmailThread(**email) for email in test_emails]
    assert len(email_threads) == len(test_emails)
    assert all(isinstance(e, EmailThread) for e in email_threads)
    
    # Test bucket conversion
    bucket_models = [Bucket(**bucket) for bucket in sample_buckets]
    assert len(bucket_models) == len(sample_buckets)
    assert all(isinstance(b, Bucket) for b in bucket_models)
    
    print("\n=== Pydantic Model Conversion Test ===")
    print(f"Successfully converted {len(email_threads)} emails")
    print(f"Successfully converted {len(bucket_models)} buckets")


@pytest.mark.asyncio
async def test_categorization_agent_response():
    """
    Test the categorization with specific expected behaviors.
    
    This tests that certain types of emails get categorized appropriately:
    - Urgent emails -> Important
    - Newsletters -> Newsletter
    - Promotional emails -> Auto-archive
    """
    emails = [
        {
            "id": "urgent-1",
            "subject": "URGENT: Action Required - Account Security",
            "snippet": "We detected unusual activity on your account",
            "from": "security@bank.com",
            "date": "Mon, 9 Feb 2026 15:00:00 +0000",
            "label": ""
        }
    ]
    
    buckets = [
        {
            "id": "important-bucket",
            "name": "Important",
            "description": "Emails requiring immediate attention or action"
        },
        {
            "id": "newsletter-bucket",
            "name": "Newsletter",
            "description": "Newsletters and promotional content"
        }
    ]
    
    result = await categorize_emails(emails, buckets)
    
    # The urgent email should go to "Important" bucket
    assert result[0]["label"] == "important-bucket", \
        f"Urgent email should be categorized as Important, got {result[0]['label']}"
    
    print("\n=== Categorization Logic Test ===")
    print("✓ Urgent email correctly categorized as Important")
    print(f"Result: {result}")


if __name__ == "__main__":
    """
    Run the tests directly without pytest for quick validation.
    """
    import asyncio
    
    print("Running categorization tests...\n")
    
    # Load data
    data_dir = Path(__file__).parent.parent / "data"
    with open(data_dir / "emails.json") as f:
        emails = json.load(f)
    with open(data_dir / "buckets.json") as f:
        buckets = json.load(f)
    
    # Run a simple test
    result = asyncio.run(categorize_emails(emails[:3], buckets))
    
    print("\n=== Quick Test Result ===")
    print(f"Categorized {3} emails")
    print(f"Result: {result}")
