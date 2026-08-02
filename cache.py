import json
import redis.asyncio as redis
from typing import Any, Optional, TypeVar, Generic
from functools import wraps
import asyncio

from backend.config.settings import get_settings
from backend.core.logging import Logger

logger = Logger(__name__)
settings = get_settings()

T = TypeVar('T')

class CacheService(Generic[T]):
    """Redis cache service"""
    
    _client: Optional[redis.Redis] = None
    
    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Get or create Redis client"""
        if cls._client is None:
            cls._client = await redis.from_url(
                settings.redis_url,
                db=settings.redis_db,
                decode_responses=True
            )
        return cls._client
    
    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set cache value"""
        try:
            client = await cls.get_client()
            serialized = json.dumps(value) if not isinstance(value, str) else value
            await client.setex(key, ttl, serialized)
            logger.debug(f"Cache set: {key}", ttl=ttl)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {key}", error=str(e))
            return False
    
    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        """Get cache value"""
        try:
            client = await cls.get_client()
            value = await client.get(key)
            
            if value is None:
                return None
            
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        
        except Exception as e:
            logger.error(f"Cache get error: {key}", error=str(e))
            return None
    
    @classmethod
    async def delete(cls, key: str) -> bool:
        """Delete cache value"""
        try:
            client = await cls.get_client()
            await client.delete(key)
            logger.debug(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {key}", error=str(e))
            return False
    
    @classmethod
    async def clear_pattern(cls, pattern: str) -> int:
        """Clear cache by pattern"""
        try:
            client = await cls.get_client()
            keys = await client.keys(pattern)
            if keys:
                await client.delete(*keys)
            logger.debug(f"Cache cleared: {pattern}", count=len(keys))
            return len(keys)
        except Exception as e:
            logger.error(f"Cache clear error: {pattern}", error=str(e))
            return 0

def cache_key(*args, **kwargs) -> str:
    """Generate cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)

def cached(ttl: int = 3600, key_prefix: str = ""):
    """Decorator for caching async functions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            full_key = f"{key_prefix or func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = await CacheService.get(full_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {full_key}")
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            await CacheService.set(full_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator