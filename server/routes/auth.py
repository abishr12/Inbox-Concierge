from config import config
from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow
from services import storage_service

router = APIRouter()


@router.get("/login")
def login():
    flow = Flow.from_client_config(
        config.get_google_client_config(),
        scopes=config.GMAIL_SCOPES,
        redirect_uri=config.REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return {"auth_url": auth_url}


@router.get("/callback")
def callback(code: str):
    flow = Flow.from_client_config(
        config.get_google_client_config(),
        scopes=config.GMAIL_SCOPES,
        redirect_uri=config.REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    storage_service.save_session({
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    })
    
    return {"status": "authenticated"}


@router.get("/status")
def status():
    session = storage_service.get_session()
    if session:
        return {"authenticated": True}
    return {"authenticated": False}


@router.post("/logout")
def logout():
    storage_service.clear_session()
    return {"status": "logged out"}
