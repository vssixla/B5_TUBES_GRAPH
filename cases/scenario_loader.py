import csv
import json
import math
from pathlib import Path
from core.graph_model import Node, Edge, SpatialGraphModel


def load_dataset(directory: Path):
    with (directory / "nodes.csv").open(encoding="utf-8-sig", newline="") as f:
        nodes = [Node(**{**r, "x": float(r["x"]), "y": float(r["y"])})
                 for r in csv.DictReader(f)]
    with (directory / "edges.csv").open(encoding="utf-8-sig", newline="") as f:
        edges = [Edge(**{**r, "delay_ms": float(r["delay_ms"])})
                 for r in csv.DictReader(f)]
    ids = {n.node_id for n in nodes}
    if not nodes or len(ids) != len(nodes) or "N01" not in ids:
        raise ValueError("Node harus unik, tidak kosong, dan memuat N01.")
    if len({e.edge_id for e in edges}) != len(edges):
        raise ValueError("ID edge harus unik; pasangan node boleh berulang.")
    for n in nodes:
        if not math.isfinite(n.x) or not math.isfinite(n.y):
            raise ValueError(f"Koordinat {n.node_id} tidak valid.")
    for e in edges:
        if e.source not in ids or e.target not in ids or e.source == e.target:
            raise ValueError(f"Endpoint {e.edge_id} tidak valid.")
        if not math.isfinite(e.delay_ms) or e.delay_ms <= 0:
            raise ValueError(f"Delay {e.edge_id} harus positif dan finite.")
    return nodes, edges


def load_scenario(path):
    """Manifest JSON menentukan dataset; modul json tersedia bawaan Python."""
    path = Path(path).resolve()
    with path.open(encoding="utf-8") as stream:
        config = json.load(stream)
    required = {"case_id", "title", "nodes_file", "edges_file", "center"}
    if not isinstance(config, dict) or not required <= config.keys():
        raise ValueError("Manifest skenario belum lengkap.")
    if config["center"] != "N01":
        raise ValueError("Skenario ini menggunakan N01 sebagai panel pusat.")
    if config["nodes_file"] != "nodes.csv" or config["edges_file"] != "edges.csv":
        raise ValueError("Dataset skenario harus bernama nodes.csv dan edges.csv.")
    nodes, edges = load_dataset(path.parent)
    for key, actual in [("expected_nodes", len(nodes)), ("expected_edges", len(edges))]:
        if key in config and config[key] != actual:
            raise ValueError(f"Jumlah dataset tidak sesuai {key}.")
    return SpatialGraphModel(nodes, edges, config["case_id"], config["title"], config["center"])
