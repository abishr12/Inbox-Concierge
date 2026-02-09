"""
Standalone test runner for categorization service.
Run this directly with: python __tests__/run_categorization_test.py
"""

import asyncio
import json
import sys
import traceback
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from services.categorization_service import categorize_emails

# Load environment variables from .env file
load_dotenv()

# Add server directory to path (parent of __tests__)
sys.path.insert(0, str(Path(__file__).parent.parent))




async def main():
    """Run categorization tests."""
    print("=" * 60)
    print("CATEGORIZATION SERVICE TEST")
    print("=" * 60)
    
    # Load test data (data directory is in parent folder)
    data_dir = Path(__file__).parent.parent / "data"
    
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
        
        # Count emails per bucket
        label_counts = Counter(email.get('label', '') for email in result)
        
        print("\n📊 Distribution:")
        for bucket in buckets:
            count = label_counts.get(bucket['id'], 0)
            print(f"  {bucket['name']}: {count} emails")
    except Exception as e:
        print(f"\n❌ Error during full categorization: {e}")
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
