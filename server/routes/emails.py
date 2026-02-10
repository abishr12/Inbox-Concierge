import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from services import categorization_service, gmail_service, storage_service

router = APIRouter()

BATCH_SIZE = 10


@router.get("/")
async def get_emails():
    """Return cached emails if available, otherwise 404"""
    session = storage_service.get_session()
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    cached_emails = storage_service.get_emails()
    if cached_emails:
        return cached_emails

    raise HTTPException(status_code=404, detail="No cached emails. Use /emails/stream for initial load.")


@router.get("/stream")
async def stream_emails():
    """Stream emails as they're categorized in batches via SSE"""
    session = storage_service.get_session()
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Check cache first
    cached_emails = storage_service.get_emails()
    if cached_emails:
        async def send_cached():
            yield f"data: {json.dumps(cached_emails)}\n\n"
        return StreamingResponse(send_cached(), media_type="text/event-stream")

    # Fetch emails from Gmail
    emails = gmail_service.get_last_threads(session, 100)
    buckets = storage_service.get_buckets()

    async def generate():
        all_categorized = []
        for i in range(0, len(emails), BATCH_SIZE):
            batch = emails[i:i + BATCH_SIZE]
            categorized_batch = await categorization_service.categorize_emails(
                batch, buckets
            )
            all_categorized.extend(categorized_batch)
            yield f"data: {json.dumps(categorized_batch)}\n\n"

        storage_service.save_emails(all_categorized)

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/recategorize-stream")
async def recategorize_stream():
    """Re-categorize all cached emails with current buckets, streaming results via SSE"""
    session = storage_service.get_session()
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    emails = storage_service.get_emails()
    if not emails:
        raise HTTPException(status_code=404, detail="No emails found")

    buckets = storage_service.get_buckets()

    # Strip old labels before re-categorizing
    for email in emails:
        email["label_id"] = ""
        email["label_name"] = ""

    async def generate():
        all_categorized = []
        for i in range(0, len(emails), BATCH_SIZE):
            batch = emails[i:i + BATCH_SIZE]
            categorized_batch = await categorization_service.categorize_emails(
                batch, buckets
            )
            all_categorized.extend(categorized_batch)
            yield f"data: {json.dumps(categorized_batch)}\n\n"

        storage_service.save_emails(all_categorized)

    return StreamingResponse(generate(), media_type="text/event-stream")
