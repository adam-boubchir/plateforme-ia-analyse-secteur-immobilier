from __future__ import annotations

from threading import Lock

__all__ = [
    "SemanticCache",
]


class SemanticCache:
    """
    In-memory cache containing business values used by the SQL Agent.

    The cache is loaded only once during the application startup.
    """

    __slots__ = (
        "_initialized",
        "_loaded",
        "_regions",
        "_provinces",
        "_communes",
        "_quartiers",
        "_materials",
        "_products",
    )

    _instance = None
    _lock = Lock()

    def __new__(cls) -> "SemanticCache":
        """
        Ensure a single cache instance (Singleton).
        """

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)
                cls._instance._initialized = False

        return cls._instance

    def __init__(self) -> None:

        if self._initialized:
            return

        self._initialized = True

        self._loaded = False

        self._regions: list[str] = []
        self._provinces: list[str] = []
        self._communes: list[str] = []
        self._quartiers: list[str] = []
        self._materials: list[str] = []
        self._products: list[str] = []

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def regions(self) -> list[str]:
        return self._regions

    @property
    def provinces(self) -> list[str]:
        return self._provinces

    @property
    def communes(self) -> list[str]:
        return self._communes

    @property
    def quartiers(self) -> list[str]:
        return self._quartiers

    @property
    def materials(self) -> list[str]:
        return self._materials

    @property
    def products(self) -> list[str]:
        return self._products

    # ==========================================================
    # Public
    # ==========================================================

    def is_loaded(self) -> bool:
        """
        Return True if the cache has already been loaded.
        """

        return self._loaded

    def mark_loaded(self) -> None:
        """
        Mark the cache as loaded.
        """

        self._loaded = True

    def reset(self) -> None:
        """
        Clear the cache.
        """

        self._clear_collections()
        self._loaded = False

    def size(self) -> int:
        """
        Return the total number of cached values.
        """

        return sum(
            len(collection)
            for collection in (
                self._regions,
                self._provinces,
                self._communes,
                self._quartiers,
                self._materials,
                self._products,
            )
        )

    def statistics(self) -> dict[str, int]:
        """
        Return cache statistics.
        """

        return {
            "regions": len(self._regions),
            "provinces": len(self._provinces),
            "communes": len(self._communes),
            "quartiers": len(self._quartiers),
            "materials": len(self._materials),
            "products": len(self._products),
        }

    # ==========================================================
    # Private
    # ==========================================================

    def _clear_collections(self) -> None:
        """
        Clear all cached collections.
        """

        for collection in (
            self._regions,
            self._provinces,
            self._communes,
            self._quartiers,
            self._materials,
            self._products,
        ):
            collection.clear()