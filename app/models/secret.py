# app/models/secret.py
from pydantic import BaseModel, Field
from typing import Optional


class SecretCreate(BaseModel):
    secret: str = Field(..., example="my super secret")
    passphrase: Optional[str] = Field(None, example="optional_passphrase")
    ttl_seconds: Optional[int] = Field(None, example=3600)


class SecretResponse(BaseModel):
    secret_key: str
