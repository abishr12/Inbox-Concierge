from pydantic import BaseModel, ConfigDict, Field


class EmailThread(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    subject: str
    snippet: str
    from_: str = Field(alias="from")
    date: str
    label_id: str
    label_name: str


class Bucket(BaseModel):
    id: str
    name: str
    description: str


class AuthStatus(BaseModel):
    authenticated: bool
    email: str | None = None


class BucketCreate(BaseModel):
    name: str
    description: str
