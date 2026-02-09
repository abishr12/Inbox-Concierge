"""
Standalone test runner for categorization service.
Run this directly with: python run_categorization_test.py
"""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add server to path
sys.path.insert(0, str(Path(__file__).parent))

from services.categorization_service import categorize_emails


async def main():
    """Run categorization tests."""
    print("=" * 60)
    print("CATEGORIZATION SERVICE TEST")
    print("=" * 60)
    
    # Load test data
    data_dir = Path(__file__).parent / "data"
    
    print("\n📂 Loading test data...")
    with open(data_dir / "emails.json") as f:
        all_emails = json.load(f)
    with open(data_dir / "buckets.json") as f:
        buckets = json.load(f)
    
    print(f"✓ Loaded {len(all_emails)} emails")
    print(f"✓ Loaded {len(buckets)} buckets")
    
    # Display bucket information
    print("\n📊 Available Buckets:")
    for bucket in buckets:
        print(f"  - {bucket['name']}: {bucket['description']}")
    
    # Test 1: Small subset
    print("\n" + "=" * 60)
    print("TEST 1: Categorizing 3 sample emails")
    print("=" * 60)
    
    test_emails = all_emails[:3]
    print("\nEmails to categorize:")
    for i, email in enumerate(test_emails, 1):
        print(f"\n{i}. From: {email['from']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Snippet: {email['snippet'][:80]}...")
    
    print("\n⏳ Running categorization agent...")
    try:
        result = await categorize_emails(test_emails, buckets)
        print("\n✅ Categorization completed!")
        print(f"\nResult type: {type(result)}")
        print(f"Result: {result}")
        
        # If result is returned (once uncommented in service)
        if result:
            print("\n📋 Categorization Results:")
            for email in result:
                bucket_name = next(
                    (b['name'] for b in buckets if b['id'] == email.get('label', '')),
                    'Unknown'
                )
                print(f"\n  • {email['subject'][:50]}...")
                print(f"    → {bucket_name}")
    except Exception as e:
        print(f"\n❌ Error during categorization: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Full email set
    print("\n" + "=" * 60)
    print("TEST 2: Categorizing all emails")
    print("=" * 60)
    
    print(f"\n⏳ Processing {len(all_emails)} emails...")
    try:
        result = await categorize_emails(all_emails, buckets)
        print("\n✅ Full categorization completed!")
        
        if result:
            # Count emails per bucket
            from collections import Counter
            label_counts = Counter(email.get('label', '') for email in result)
            
            print("\n📊 Distribution:")
            for bucket in buckets:
                count = label_counts.get(bucket['id'], 0)
                print(f"  {bucket['name']}: {count} emails")
    except Exception as e:
        print(f"\n❌ Error during full categorization: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
