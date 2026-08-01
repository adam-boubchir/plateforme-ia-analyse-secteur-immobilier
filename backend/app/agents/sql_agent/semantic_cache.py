from threading import Lock


class SemanticCache:
    """
    In-memory cache containing business values used by the SQL Agent.

    The cache is loaded only once during the application startup.
    """

    _instance = None
    _lock = Lock()

    def __new__(
        cls,
    ):
        """
        Ensure a single cache instance (Singleton).
        """

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)
                cls._instance._initialized = False

        return cls._instance

    def __init__(
        self,
    ):
        """
        Initialize the cache only once.
        """

        if self._initialized:
            return

        self._initialized = True

        self.loaded = False

        self.regions: list[str] = []
        self.provinces: list[str] = []
        self.communes: list[str] = []
        self.quartiers: list[str] = []
        self.materials: list[str] = []
        self.products: list[str] = []

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def is_loaded(
        self,
    ) -> bool:
        """
        Return True if the cache has already been loaded.
        """

        return self.loaded

    def mark_loaded(
        self,
    ) -> None:
        """
        Mark the cache as loaded.
        """

        self.loaded = True

    def clear(
        self,
    ) -> None:
        """
        Clear every cached business value.
        """

        self._clear_collections()

        self.loaded = False

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _clear_collections(
        self,
    ) -> None:
        """
        Clear all cached collections.
        """

        collections = (
            self.regions,
            self.provinces,
            self.communes,
            self.quartiers,
            self.materials,
            self.products,
        )

        for collection in collections:
            collection.clear()