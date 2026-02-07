from fastapi import APIRouter, HTTPException
from models.schemas import BucketCreate
from services import storage_service, categorization_service

router = APIRouter()


@router.get("/")
def get_buckets():
    return storage_service.get_buckets()


@router.post("/")
def add_bucket(bucket: BucketCreate):
    buckets = storage_service.get_buckets()
    if bucket.name in buckets:
        raise HTTPException(status_code=400, detail="Bucket already exists")
    
    buckets.append(bucket.name)
    storage_service.save_buckets(buckets)
    
    emails = storage_service.get_emails()
    if emails:
        categorized_emails = categorization_service.categorize_emails(emails, buckets)
        storage_service.save_emails(categorized_emails)
        return categorized_emails
    
    return []


@router.delete("/{bucket_name}")
def remove_bucket(bucket_name: str):
    buckets = storage_service.get_buckets()
    if bucket_name not in buckets:
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    buckets.remove(bucket_name)
    storage_service.save_buckets(buckets)
    
    emails = storage_service.get_emails()
    if emails:
        categorized_emails = categorization_service.categorize_emails(emails, buckets)
        storage_service.save_emails(categorized_emails)
        return categorized_emails
    
    return []
