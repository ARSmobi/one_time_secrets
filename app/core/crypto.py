# app/core/crypto.py
from cryptography.fernet import Fernet

class CryptoService:
    def __init__(self, key: bytes):
        self._fernet = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token.encode()).decode()


# Генерация ключа (обычно один раз и хранится в .env)
fernet_key = Fernet.generate_key()
crypto_service = CryptoService(fernet_key)
