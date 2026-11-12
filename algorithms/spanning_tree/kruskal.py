def KruskalMST(node_ids, edges, trace=False, start="N01"):
    uf = UnionFind(node_ids)
    selected, steps, checks = [], [], 0
    for edge in sorted(edges, key=lambda e: (e.delay_ms, e.edge_id)):
        checks += 1
        if trace:
            steps.append({"kind": "consider", "edge_id": edge.edge_id,
                          "message": f"Periksa {edge.edge_id}: {edge.delay_ms:g} ms (urutan bobot)."})
        accepted = uf.union(edge.source, edge.target)
        if accepted:
            selected.append(edge)
        if trace:
            steps.append({"kind": "accept" if accepted else "reject", "edge_id": edge.edge_id,
                          "message": (f"Pilih {edge.edge_id}: menggabungkan dua komponen."
                                      if accepted else f"Tolak {edge.edge_id}: membentuk siklus.")})
        if uf.count == 1:
            break
    if trace:
        steps.append({"kind": "finish", "message": f"Selesai: {len(selected)} edge, {uf.count} komponen."})
    return {"selected_edge_ids": [e.edge_id for e in selected],
            "total_weight": sum(e.delay_ms for e in selected), "trace": steps,
            "operations": {"edge_checks": checks}}