import uuid

from fastapi import APIRouter, HTTPException
from models.schemas import BucketCreate
from services import storage_service

router = APIRouter()


@router.get("/")
def get_buckets():
    return storage_service.get_buckets()


@router.post("/")
def add_bucket(bucket: BucketCreate):
    buckets = storage_service.get_buckets()

    if any(b["name"] == bucket.name for b in buckets):
        raise HTTPException(status_code=400, detail="Bucket already exists")

    new_bucket = {
        "id": str(uuid.uuid4()),
        "name": bucket.name,
        "description": bucket.description,
    }
    buckets.append(new_bucket)
    storage_service.save_buckets(buckets)

    return new_bucket


@router.post("/{bucket_id}")
def remove_bucket(bucket_id: str):
    buckets = storage_service.get_buckets()

    bucket_to_remove = next((b for b in buckets if b["id"] == bucket_id), None)
    if not bucket_to_remove:
        raise HTTPException(status_code=404, detail="Bucket not found")

    buckets.remove(bucket_to_remove)
    storage_service.save_buckets(buckets)

    return {"success": True, "deleted_bucket_id": bucket_id, "deleted_bucket_name": bucket_to_remove["name"]}
