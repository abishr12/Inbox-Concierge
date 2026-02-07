from pydantic import BaseModel


class EmailThread(BaseModel):
    id: str
    subject: str
    snippet: str
    from_: str
    date: str
    category: str


class Bucket(BaseModel):
    name: str


class AuthStatus(BaseModel):
    authenticated: bool
    email: str | None = None


class BucketCreate(BaseModel):
    name: str
