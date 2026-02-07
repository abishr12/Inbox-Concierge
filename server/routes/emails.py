from fastapi import APIRouter, HTTPException
from services import categorization_service, gmail_service, storage_service

router = APIRouter()


@router.get("/")
def get_emails():
    session = storage_service.get_session()
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    cached_emails = storage_service.get_emails()
    if cached_emails:
        return cached_emails
    
    emails = gmail_service.get_last_threads(session, 10)
    # buckets = storage_service.get_buckets()
    # categorized_emails = categorization_service.categorize_emails(emails, buckets)
    
    # storage_service.save_emails(categorized_emails)
    # return categorized_emails
    print(emails)
    return


@router.post("/recategorize")
def recategorize_emails():
    session = storage_service.get_session()
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    emails = storage_service.get_emails()
    if not emails:
        raise HTTPException(status_code=404, detail="No emails found")
    
    buckets = storage_service.get_buckets()
    categorized_emails = categorization_service.categorize_emails(emails, buckets)
    
    storage_service.save_emails(categorized_emails)
    return categorized_emails
