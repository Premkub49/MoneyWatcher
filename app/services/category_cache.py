"""
In-memory category cache.
Loaded at startup, updated on add/delete. O(1) lookups, no DB queries.
"""

from app.models.enums import CategoryType


class _CategoryCacheEntry:
    """Lightweight object representing a cached category."""
    __slots__ = ("id", "name", "display_name", "type")

    def __init__(self, id: int, name: str, display_name: str, type: CategoryType):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.type = type


# ── global cache (keyed by name for O(1) lookup) ─────────────
_cache_by_name: dict[str, _CategoryCacheEntry] = {}
_cache_by_id: dict[int, _CategoryCacheEntry] = {}


def _put(entry: _CategoryCacheEntry):
    _cache_by_name[entry.name] = entry
    _cache_by_id[entry.id] = entry


def _remove(name: str):
    entry = _cache_by_name.pop(name, None)
    if entry:
        _cache_by_id.pop(entry.id, None)


# ── public API ────────────────────────────────────────────────

def load_cache(categories) -> None:
    """Populate cache from DB rows. Called once at startup."""
    _cache_by_name.clear()
    _cache_by_id.clear()
    for cat in categories:
        _put(_CategoryCacheEntry(
            id=cat.id,
            name=cat.name,
            display_name=cat.display_name,
            type=cat.type,
        ))
    print(f"Category cache loaded: {len(_cache_by_name)} entries")


def add_to_cache(cat) -> None:
    """Add a single category to cache after DB insert."""
    _put(_CategoryCacheEntry(
        id=cat.id,
        name=cat.name,
        display_name=cat.display_name,
        type=cat.type,
    ))


def remove_from_cache(name: str) -> None:
    """Remove a category from cache after DB delete."""
    _remove(name)


def get_by_name(name: str) -> _CategoryCacheEntry | None:
    """Look up a category by name. Returns entry or None."""
    return _cache_by_name.get(name)


def get_by_id(category_id: int) -> _CategoryCacheEntry | None:
    """Look up a category by id. Returns entry or None."""
    return _cache_by_id.get(category_id)


def get_all() -> list[_CategoryCacheEntry]:
    """Get all cached categories."""
    return list(_cache_by_name.values())
