"""
src/predictions/cache.py
Cache layer cho prediction requests.
Dùng cachetools TTLCache — không cần Redis, thread-safe với lock.
"""
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
    """
    Tạo cache key từ danh sách request.
    Dùng SHA-256 của JSON serialized (sort_keys để đảm bảo thứ tự nhất quán).
    """
    payload = json.dumps(
        [r.model_dump() for r in requests],
        sort_keys=True,
        ensure_ascii=False
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def get_cached(requests: List[Any]) -> Optional[List[dict]]:
    """
    Trả về kết quả cache nếu có, None nếu không có.
    """
    key = _make_cache_key(requests)
    with _lock:
        return _cache.get(key)


def set_cached(requests: List[Any], result: List[dict]) -> None:
    """
    Lưu kết quả vào cache.
    """
    key = _make_cache_key(requests)
    with _lock:
        _cache[key] = result


def get_cache_info() -> dict:
    """
    Trả về thông tin trạng thái cache (dùng cho monitoring endpoint).
    """
    with _lock:
        return {
            "current_size": len(_cache),
            "max_size": _cache.maxsize,
            "ttl_seconds": CACHE_TTL_SECONDS,
        }


def clear_cache() -> None:
    """
    Xóa toàn bộ cache (dùng khi deploy model mới).
    """
    with _lock:
        _cache.clear()