"""
Caching layer supporting in-memory TTL cache with optional Redis backend.
Designed to guarantee sub-50ms API responses for iOS client queries.
"""
import time
import json
import logging
from typing import Any, Optional
from api.config import settings

logger = logging.getLogger("avdb_api.cache")

class MemoryCache:
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        expires_at, value = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self.default_ttl
        self._store[key] = (time.time() + duration, value)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        # Purge expired entries on count
        now = time.time()
        expired = [k for k, (exp, _) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(self._store)


class RedisCache:
    def __init__(self, redis_url: str, default_ttl: int = 3600):
        import redis
        self.default_ttl = default_ttl
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        try:
            val = self.client.get(key)
            if val is not None:
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis get failed for {key}: {e}")
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        try:
            duration = ttl if ttl is not None else self.default_ttl
            self.client.setex(key, duration, json.dumps(value, default=str))
        except Exception as e:
            logger.warning(f"Redis set failed for {key}: {e}")

    def clear(self) -> None:
        try:
            self.client.flushdb()
        except Exception as e:
            logger.warning(f"Redis clear failed: {e}")

    def size(self) -> int:
        try:
            return self.client.dbsize()
        except Exception:
            return 0


# Factory initialization
_cache_instance = None

def get_cache():
    global _cache_instance
    if _cache_instance is None:
        if settings.redis_url:
            try:
                _cache_instance = RedisCache(settings.redis_url, default_ttl=settings.cache_ttl_seconds)
                logger.info("Initialized Redis cache backend")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis, falling back to MemoryCache: {e}")
                _cache_instance = MemoryCache(default_ttl=settings.cache_ttl_seconds)
        else:
            _cache_instance = MemoryCache(default_ttl=settings.cache_ttl_seconds)
            logger.info("Initialized in-memory TTL cache backend")
    return _cache_instance
