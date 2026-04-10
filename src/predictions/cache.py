import hashlib
import json
from cachetools import TTLCache
from threading import Lock
from typing import List, Optional, Any

CACHE_MAX_SIZE = 512    
CACHE_TTL_SECONDS = 300 

_cache: TTLCache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)
_lock = Lock()         

def _make_cache_key(requests: List[Any]) -> str:
    payload = json.dumps(
        [r.model_dump() for r in requests],
        sort_keys=True,
        ensure_ascii=False
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def get_cached(requests: List[Any]) -> Optional[List[dict]]:
    key = _make_cache_key(requests)
    with _lock:
        return _cache.get(key)


def set_cached(requests: List[Any], result: List[dict]) -> None:
    key = _make_cache_key(requests)
    with _lock:
        _cache[key] = result


def get_cache_info() -> dict:
    with _lock:
        return {
            "current_size": len(_cache),
            "max_size": _cache.maxsize,
            "ttl_seconds": CACHE_TTL_SECONDS,
        }


def clear_cache() -> None:
    with _lock:
        _cache.clear()