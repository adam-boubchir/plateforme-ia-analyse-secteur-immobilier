from threading import Lock


class SemanticCache:
    """
    Cache mémoire contenant les valeurs métier utilisées
    par le SQL Agent.

    Le cache est chargé une seule fois au démarrage
    de l'application.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)

                cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self._initialized = True

        self.loaded = False

        self.regions = []

        self.provinces = []

        self.communes = []

        self.quartiers = []

        self.materials = []

        self.products = []

    def is_loaded(self) -> bool:

        return self.loaded

    def mark_loaded(self):

        self.loaded = True

    def clear(self):

        self.regions.clear()

        self.provinces.clear()

        self.communes.clear()

        self.quartiers.clear()

        self.materials.clear()

        self.products.clear()

        self.loaded = False