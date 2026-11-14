"""Kontrak algoritma dan pencatatan event yang diputar oleh dashboard."""
from abc import ABC, abstractmethod
from collections import Counter


class BaseAlgorithm(ABC):
    name: str

    @staticmethod
    @abstractmethod
    def run(node_ids, edges, trace=False, start="N01"):
        """Kembalikan selected_edge_ids, total_weight, trace, dan operations."""
        raise NotImplementedError


class TraceLogger:
    """Hanya merekam jejak ketika trace=True; benchmark menonaktifkannya."""
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps = []
        self.counts = Counter()

    def record(self, event):
        if self.enabled:
            self.steps.append(event)
            self.counts[event["kind"]] += 1
