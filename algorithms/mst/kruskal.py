#Implementasi Kruskal Algoritma
from core.base_algorithm import BaseAlgorithm, TraceLogger
from .union_find import UnionFind

def kruskal(node_ids, edges, trace=False, start="N01"):
    uf = UnionFind(node_ids)
    selected, checks = [], 0
    logger = TraceLogger(trace)
    steps = logger.steps
    for edge in sorted(edges, key=lambda e: (e.delay_ms, e.edge_id)):
        checks += 1
        if trace:
            logger.record({"kind": "consider", "edge_id": edge.edge_id,
                          "message": f"Periksa {edge.edge_id}: {edge.delay_ms:g} ms (urutan bobot)."})
        accepted = uf.union(edge.source, edge.target)
        if accepted:
            selected.append(edge)
        if trace:
            logger.record({"kind": "accept" if accepted else "reject", "edge_id": edge.edge_id,
                          "message": (f"Pilih {edge.edge_id}: menggabungkan dua komponen."
                                      if accepted else f"Tolak {edge.edge_id}: membentuk siklus.")})
        if uf.count == 1:
            break
    if trace:
        logger.record({"kind": "finish", "message": f"Selesai: {len(selected)} edge, {uf.count} komponen."})
    return {"selected_edge_ids": [e.edge_id for e in selected],
            "total_weight": sum(e.delay_ms for e in selected), "trace": steps,
            "operations": {"edge_checks": checks}, "event_counts": logger.counts}

class KruskalAlgorithm(BaseAlgorithm):
    name = "kruskal"
    run = staticmethod(kruskal)
