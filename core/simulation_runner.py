"""Satu snapshot graf aktif untuk kedua algoritma; tanpa state global sesi."""
from collections import defaultdict
from statistics import median
from time import perf_counter_ns
import math
from algorithms.registry import ALGORITHMS
from algorithms.mst.kruskal import kruskal
from config.settings import BENCHMARK_ROUNDS, BENCHMARK_BATCH_SIZE, WARMUP_RUNS
from .analysis import connected_components, evaluate


def benchmark(node_ids, edges, rounds=BENCHMARK_ROUNDS, batch_size=BENCHMARK_BATCH_SIZE):
    # Pemanasan dan urutan bergantian mengurangi bias urutan eksekusi.
    for function in ALGORITHMS.values():
        for _ in range(WARMUP_RUNS):
            function(node_ids, edges)
    samples = {name: [] for name in ALGORITHMS}
    for round_no in range(rounds):
        names = list(ALGORITHMS)
        if round_no % 2:
            names.reverse()
        for name in names:
            function = ALGORITHMS[name]
            start = perf_counter_ns()
            for _ in range(batch_size):
                function(node_ids, edges, trace=False)
            elapsed = perf_counter_ns() - start
            samples[name].append(elapsed / batch_size / 1_000_000)
    return {name: median(values) for name, values in samples.items()}


class SimulationRunner:
    def __init__(self, graph, observers=()):
        self.graph = graph
        self.observers = tuple(observers)
        nodes, edges = graph.nodes, graph.edges
        self.nodes, self.edges = nodes, edges
        self.node_ids = [n.node_id for n in nodes]
        self.edge_ids = {e.edge_id for e in edges}
        if len(connected_components(self.node_ids, edges)) != 1:
            raise ValueError("Dataset awal harus terhubung untuk baseline MST.")
        self.baseline_weight = kruskal(self.node_ids, edges)["total_weight"]

    def dataset(self):
        pairs = defaultdict(list)
        for e in self.edges:
            pairs[tuple(sorted((e.source, e.target)))].append(e.edge_id)
        return {"nodes": [n.to_dict() for n in self.nodes], "edges": [e.to_dict() for e in self.edges],
                "center": "N01", "baseline_weight_ms": self.baseline_weight,
                "parallel_groups": [ids for ids in pairs.values() if len(ids) > 1]}

    def compute(self, failed_ids):
        if not isinstance(failed_ids, list) or any(not isinstance(x, str) for x in failed_ids):
            raise ValueError("failed_edge_ids harus berupa array ID edge.")
        if len(set(failed_ids)) != len(failed_ids):
            raise ValueError("Edge yang sama tidak boleh diputus dua kali.")
        if set(failed_ids) - self.edge_ids:
            raise ValueError("Ada ID edge yang tidak dikenal.")
        failed = set(failed_ids)
        active = self.graph.active_edges(failed)
        components = connected_components(self.node_ids, active)
        reachable = next(c for c in components if "N01" in c)
        times = benchmark(self.node_ids, active)
        results = {}
        for name, function in ALGORITHMS.items():
            result = function(self.node_ids, active, trace=True)
            result.update(evaluate(self.nodes, active, result, components, self.baseline_weight))
            result["computation_ms"] = times[name]
            results[name] = result
        if not math.isclose(results["kruskal"]["total_weight"], results["prim"]["total_weight"], abs_tol=1e-9):
            raise ValueError("Validasi gagal: total bobot kedua algoritma berbeda.")
        report = {"iteration": len(failed_ids), "newly_failed_edge": failed_ids[-1] if failed_ids else None,
                "failed_edge_ids": failed_ids, "node_count": len(self.nodes), "active_edge_count": len(active),
                "failed_edge_count": len(failed), "component_count": len(components), "components": components,
                "connected": len(components) == 1, "center_reachable_nodes": reachable,
                "center_reachable_count": len(reachable), "center_connectivity_percent": len(reachable) / len(self.nodes) * 100,
                "unreachable_nodes": sorted(set(self.node_ids) - set(reachable)),
                "baseline_weight_ms": self.baseline_weight, "results": results,
                "benchmark": {"rounds": BENCHMARK_ROUNDS, "batch_size": BENCHMARK_BATCH_SIZE, "statistic": "median", "animation_included": False},
                "validation_passed": True}

        for observer in self.observers:
            observer.on_result(report)
        return report
