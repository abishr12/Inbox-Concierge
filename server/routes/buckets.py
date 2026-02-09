import uuid

from fastapi import APIRouter, HTTPException
from models.schemas import BucketCreate
from services import categorization_service, storage_service

router = APIRouter()


@router.get("/")
def get_buckets():
    return storage_service.get_buckets()


@router.post("/")
async def add_bucket(bucket: BucketCreate):
    buckets = storage_service.get_buckets()
    
    # Check if bucket name already exists
    if any(b["name"] == bucket.name for b in buckets):
        raise HTTPException(status_code=400, detail="Bucket already exists")
    
    # Create new bucket with UUID
    new_bucket = {
        "id": str(uuid.uuid4()),
        "name": bucket.name,
        "description": bucket.description
    }
    buckets.append(new_bucket)
    storage_service.save_buckets(buckets)
    
    # Recategorize emails with updated buckets
    emails = storage_service.get_emails()
    if emails:
        categorized_emails = await categorization_service.categorize_emails(emails, buckets)
        storage_service.save_emails(categorized_emails)
        return categorized_emails
    
    return []


@router.post("/{bucket_id}")
async def remove_bucket(bucket_id: str):
    buckets = storage_service.get_buckets()

    # Find bucket by ID
    bucket_to_remove = next((b for b in buckets if b["id"] == bucket_id), None)
    if not bucket_to_remove:
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    buckets.remove(bucket_to_remove)
    storage_service.save_buckets(buckets)

    # Only recategorize emails that were in the deleted bucket
    all_emails = storage_service.get_emails()
    if not all_emails:
        return []

    # Find emails that need recategorization
    affected_emails = [e for e in all_emails if e.get("category_id") == bucket_id]

    # If no emails were in the deleted bucket, return all emails unchanged
    if not affected_emails:
        return all_emails

    # Recategorize only the affected emails
    recategorized_emails = await categorization_service.categorize_emails(
        affected_emails, buckets
    )

    # Create a lookup map of the recategorized results
    recategorized_map = {e["id"]: e for e in recategorized_emails}

    # Update the category fields in place for affected emails
    for email in all_emails:
        if email["id"] in recategorized_map:
            email["category_id"] = recategorized_map[email["id"]]["category_id"]
            email["category_name"] = recategorized_map[email["id"]]["category_name"]

    storage_service.save_emails(all_emails)
    return all_emails
