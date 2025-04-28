# app/api/secrets.py
from fastapi import APIRouter, Request
from uuid import uuid4
from app.storage.memory import storage
from fastapi import HTTPException

from app.models.secret import SecretCreate, SecretResponse
from app.core.crypto import crypto_service

router = APIRouter()


@router.post("/secret", response_model=SecretResponse)
async def create_secret(payload: SecretCreate, request: Request):
    # Пока просто генерируем ключ, позже добавим логику шифрования, кэш и БД
    secret_key = str(uuid4())
    ttl = payload.ttl_seconds or 300  # 5 минут по умолчанию
    encrypted_secret = crypto_service.encrypt(payload.secret)
    # Записываем зашифрованный секрет в кэш и устанавливаем время жизни
    storage.set(secret_key, encrypted_secret, ttl=ttl)
    return SecretResponse(secret_key=secret_key)

@router.get("/secret/{secret_key}")
async def get_secret(secret_key: str, request: Request):
    encrypted_secret = storage.get_and_delete(secret_key)
    if encrypted_secret is None:
        raise HTTPException(status_code=404, detail="Secret not found or already read")
    try:
        decrypted_secret = crypto_service.decrypt(encrypted_secret)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decrypt secret")
    return {"secret": decrypted_secret}