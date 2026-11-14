"""Konektivitas graf aktif dan delay rute pada pohon hasil algoritma."""
import math
from algorithms.mst.union_find import UnionFind

SENSOR_TYPES = {"Smoke Detector", "Heat Detector", "Temperature Sensor",
                "Temperature-Humidity Sensor", "Detektor Api"}


def connected_components(node_ids, edges):
    uf = UnionFind(node_ids)
    for edge in edges:
        uf.union(edge.source, edge.target)
    groups = {}
    for node in sorted(node_ids):
        groups.setdefault(uf.find(node), []).append(node)
    return sorted(groups.values(), key=lambda group: ("N01" not in group, group[0]))


def evaluate(nodes, active_edges, result, components, baseline_weight, center="N01"):
    edge_map = {e.edge_id: e for e in active_edges}
    chosen_ids = result["selected_edge_ids"]
    if len(set(chosen_ids)) != len(chosen_ids) or any(e not in edge_map for e in chosen_ids):
        raise ValueError("Hasil menggunakan edge duplikat atau tidak aktif.")
    uf = UnionFind(n.node_id for n in nodes)
    tree = {n.node_id: [] for n in nodes}
    for edge_id in chosen_ids:
        e = edge_map[edge_id]
        if not uf.union(e.source, e.target):
            raise ValueError("Hasil mengandung siklus.")
        tree[e.source].append((e.target, e.delay_ms, e.edge_id))
        tree[e.target].append((e.source, e.delay_ms, e.edge_id))
    if len(chosen_ids) != len(nodes) - len(components):
        raise ValueError("Hasil tidak merentangkan semua komponen.")
    weight = sum(edge_map[e].delay_ms for e in chosen_ids)
    if not math.isclose(weight, result["total_weight"], abs_tol=1e-9):
        raise ValueError("Bobot hasil tidak cocok dengan edge terpilih.")
    # Setiap komponen hasil adalah subset komponen input. Forest dengan n-k
    # edge berarti seluruh k komponen input direntangkan.
    paths = {center: (0.0, [center], [])}
    stack = [center]
    while stack:
        node = stack.pop()
        distance, route, route_edges = paths[node]
        for neighbor, delay, edge_id in tree[node]:
            if neighbor not in paths:
                paths[neighbor] = (distance + delay, route + [neighbor], route_edges + [edge_id])
                stack.append(neighbor)
    sensors = []
    for n in nodes:
        if n.device_name not in SENSOR_TYPES:
            continue
        path = paths.get(n.node_id)
        sensors.append({"node_id": n.node_id, "device_name": n.device_name, "area": n.area,
                        "delay_ms": path[0] if path else None,
                        "path": list(reversed(path[1])) if path else [],
                        "edge_ids": list(reversed(path[2])) if path else []})
    reachable_delays = [s["delay_ms"] for s in sensors if s["delay_ms"] is not None]
    connected = len(components) == 1
    delta = weight - baseline_weight if connected else None
    return {"selected_edge_count": len(chosen_ids), "total_mst_delay_ms": weight if connected else None,
            "total_msf_delay_ms": weight if not connected else None,
            "delta_ms": delta, "delta_percent": delta / baseline_weight * 100 if delta is not None and baseline_weight else None,
            "sensor_paths": sensors,
            "average_sensor_delay_ms": sum(reachable_delays) / len(reachable_delays) if reachable_delays else None,
            "max_sensor_delay_ms": max(reachable_delays) if reachable_delays else None,
            "unreachable_sensor_count": len(sensors) - len(reachable_delays),
            "validation_passed": True}
