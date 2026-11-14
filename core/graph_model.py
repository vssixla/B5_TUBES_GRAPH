"""Membaca CSV tanpa menggabungkan edge paralel."""
import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Node:
    node_id: str
    device_name: str
    area: str
    floor: str
    function: str
    x: float
    y: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Edge:
    edge_id: str
    source: str
    target: str
    delay_ms: float
    edge_type: str = "alternative"

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class SpatialGraphModel:
    nodes: list[Node]
    edges: list[Edge]
    case_id: str = "case_26_gudang_terbakar"
    title: str = "Gudang Terbakar (MST)"
    center: str = "N01"

    @property
    def node_ids(self):
        return [node.node_id for node in self.nodes]

    def active_edges(self, failed_ids):
        failed = set(failed_ids)
        return [edge for edge in self.edges if edge.edge_id not in failed]
