from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, emails, buckets

app = FastAPI(title="Email Concierge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(emails.router, prefix="/emails", tags=["emails"])
app.include_router(buckets.router, prefix="/buckets", tags=["buckets"])


@app.get("/")
def read_root():
    return {"message": "Email Concierge API"}
