# app/storage/memory.py
import time
from typing import Optional
from threading import Lock


class SecretData:
    def __init__(self, secret: str, expires_at: float):
        self.secret = secret
        self.expires_at = expires_at


class InMemoryStorage:
    def __init__(self):
        self._storage = {}
        self._lock = Lock()

    def set(self, key: str, value: str, ttl: int = 300):
        expires_at = time.time() + ttl
        with self._lock:
            self._storage[key] = SecretData(secret=value, expires_at=expires_at)

    def get_and_delete(self, key: str) -> Optional[str]:
        with self._lock:
            data = self._storage.get(key)
            if data and data.expires_at > time.time():
                del self._storage[key]
                return data.secret
            # Удалим, даже если просрочено
            if key in self._storage:
                del self._storage[key]
            return None

    def delete(self, key: str):
        with self._lock:
            self._storage.pop(key, None)


# Экземпляр хранилища
storage = InMemoryStorage()
