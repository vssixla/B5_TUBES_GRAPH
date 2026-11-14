"""Observer hasil simulasi untuk CLI dan ekspor JSON."""
import json
from pathlib import Path


class ConsoleObserver:
    def on_result(self, report):
        state = "MST" if report["connected"] else "MSF"
        print(f"Iterasi {report['iteration']} | {state} | {report['component_count']} komponen")
        for name, result in report["results"].items():
            print(f"  {name.title():7} : {result['selected_edge_count']} edge, "
                  f"bobot {result['total_weight']:g} ms, "
                  f"komputasi {result['computation_ms']:.4f} ms")


class JsonTraceObserver:
    """Menyimpan rangkaian snapshot dan seluruh event kedua algoritma."""
    def __init__(self, path):
        self.path = Path(path)
        self.reports = []

    def on_result(self, report):
        self.reports.append(report)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.reports, ensure_ascii=False, indent=2), encoding="utf-8")
