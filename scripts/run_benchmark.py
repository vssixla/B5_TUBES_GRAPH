"""python -m scripts.run_benchmark --fail E28 E29 E38 --export output/benchmark.csv"""
import argparse
import csv
from pathlib import Path
from cases.scenario_loader import load_scenario
from config.settings import DEFAULT_SCENARIO
from core.simulation_runner import SimulationRunner


def main():
    parser = argparse.ArgumentParser(description="Benchmark dua algoritma pada snapshot identik.")
    parser.add_argument("--scenario", default=str(DEFAULT_SCENARIO))
    parser.add_argument("--fail", nargs="*", default=[])
    parser.add_argument("--export", help="Lokasi hasil CSV.")
    args = parser.parse_args()
    runner = SimulationRunner(load_scenario(args.scenario))
    if len(set(args.fail)) != len(args.fail) or set(args.fail) - runner.edge_ids:
        parser.error("Urutan kerusakan harus berisi ID edge unik yang tersedia.")
    rows = []
    for iteration in range(len(args.fail) + 1):
        report = runner.compute(args.fail[:iteration])
        for name, result in report["results"].items():
            row = {"iteration": iteration, "algorithm": name,
                   "newly_failed_edge": report["newly_failed_edge"] or "",
                   "active_edges": report["active_edge_count"], "components": report["component_count"],
                   "result_type": "MST" if report["connected"] else "MSF",
                   "selected_edges": result["selected_edge_count"], "total_weight_ms": result["total_weight"],
                   "computation_ms": result["computation_ms"], "edge_checks": result["operations"]["edge_checks"],
                   "trace_events": len(result["trace"])}
            rows.append(row)
            print(f"{iteration:2} | {name:7} | {row['computation_ms']:.4f} ms | "
                  f"{row['edge_checks']:3} edge checks | {row['trace_events']:3} events")
    if args.export:
        path = Path(args.export)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
