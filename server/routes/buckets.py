from fastapi import APIRouter, HTTPException
from models.schemas import BucketCreate
from services import storage_service, categorization_service
import uuid

router = APIRouter()


@router.get("/")
def get_buckets():
    return storage_service.get_buckets()


@router.post("/")
def add_bucket(bucket: BucketCreate):
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
        bucket_names = [b["name"] for b in buckets]
        categorized_emails = categorization_service.categorize_emails(emails, bucket_names)
        storage_service.save_emails(categorized_emails)
        return categorized_emails
    
    return []


@router.delete("/{bucket_name}")
def remove_bucket(bucket_name: str):
    buckets = storage_service.get_buckets()
    
    # Find bucket by name
    bucket_to_remove = next((b for b in buckets if b["name"] == bucket_name), None)
    if not bucket_to_remove:
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    buckets.remove(bucket_to_remove)
    storage_service.save_buckets(buckets)
    
    # Recategorize emails with updated buckets
    emails = storage_service.get_emails()
    if emails:
        bucket_names = [b["name"] for b in buckets]
        categorized_emails = categorization_service.categorize_emails(emails, bucket_names)
        storage_service.save_emails(categorized_emails)
        return categorized_emails
    
    return []
