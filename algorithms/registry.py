# Algoritma MST yang digunakan oleh dashboard dan runner CLI.
from .mst.kruskal import KruskalAlgorithm
from .mst.prim import PrimAlgorithm


class AlgorithmRegistry:
    _classes = {"kruskal": KruskalAlgorithm, "prim": PrimAlgorithm}

    @classmethod
    def create(cls, name):
        key = name.strip().lower()
        if key not in cls._classes:
            raise ValueError(f"Algoritma tidak dikenal: {name}. Pilih kruskal atau prim.")
        return cls._classes[key]()


ALGORITHMS = {name: AlgorithmRegistry.create(name).run for name in ("kruskal", "prim")}
