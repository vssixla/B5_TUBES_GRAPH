def primMST(node_ids, edges, trace=False, start="N01"):
    adjacency = {n: [] for n in node_ids}
    for edge in edges:
        adjacency[edge.source].append((edge.target, edge))
        adjacency[edge.target].append((edge.source, edge))
    visited, selected, steps = set(), [], []
    checks = components = 0

    # Restart dari node belum dikunjungi agar semua komponen menghasilkan MSF.
    roots = ([start] if start in adjacency else []) + sorted(n for n in node_ids if n != start)
    for root in roots:
        if root in visited:
            continue
        components += 1
        visited.add(root)
        heap = []

        def add_frontier(node):
            for neighbor, edge in adjacency[node]:
                if neighbor not in visited:
                    heappush(heap, (edge.delay_ms, edge.edge_id, node, neighbor, edge))

        if trace:
            steps.append({"kind": "root", "node_id": root,
                          "message": f"Mulai komponen {components} dari {root}."})
        add_frontier(root)
        while heap:
            _, _, source, target, edge = heappop(heap)
            checks += 1
            if trace:
                steps.append({"kind": "consider", "edge_id": edge.edge_id,
                              "message": f"Ambil {edge.edge_id} ({edge.delay_ms:g} ms) dari min-heap."})
            if target in visited:
                if trace:
                    steps.append({"kind": "reject", "edge_id": edge.edge_id,
                                  "message": f"Lewati {edge.edge_id}: kedua node sudah di pohon."})
                continue
            visited.add(target)
            selected.append(edge)
            if trace:
                steps.append({"kind": "accept", "edge_id": edge.edge_id, "node_id": target,
                              "message": f"Pilih {edge.edge_id}: perluas pohon dari {source} ke {target}."})
            add_frontier(target)
    if trace:
        steps.append({"kind": "finish", "message": f"Selesai: {len(selected)} edge, {components} komponen."})
    return {"selected_edge_ids": [e.edge_id for e in selected],
            "total_weight": sum(e.delay_ms for e in selected), "trace": steps,
            "operations": {"edge_checks": checks}}