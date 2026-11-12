# Server lokal Python, standard library
import argparse
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from cases.scenario_loader import load_scenario
from core.simulation_runner import SimulationRunner
from config.settings import ROOT, STATIC_DIR, DEFAULT_SCENARIO, DEFAULT_PORT

def build_handler(simulator):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

        def send_json(self, value, status=200):
            data = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/api/graph":
                return self.send_json(simulator.dataset())
            if path.startswith("/api/"):
                return self.send_json({"error": "Endpoint tidak ditemukan."}, 404)
            return super().do_GET()

        def do_POST(self):
            if urlsplit(self.path).path != "/api/compute":
                return self.send_json({"error": "Endpoint tidak ditemukan."}, 404)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 16000:
                    raise ValueError("Ukuran request tidak valid.")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict) or "failed_edge_ids" not in payload:
                    raise ValueError("Request harus memuat failed_edge_ids.")
                result = simulator.compute(payload["failed_edge_ids"])
                self.send_json(result)
            except (ValueError, TypeError, UnicodeDecodeError) as exc:
                self.send_json({"error": str(exc)}, 400)
            except Exception:
                self.send_json({"error": "Perhitungan gagal. Periksa terminal server."}, 500)
                raise

    return Handler


def create_server(host="127.0.0.1", port=DEFAULT_PORT):
    simulator = SimulationRunner(load_scenario(DEFAULT_SCENARIO))
    return ThreadingHTTPServer((host, port), build_handler(simulator))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Warehouse MST Simulator")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", str(DEFAULT_PORT))))
    parser.add_argument("--strictPort", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"Warehouse MST Simulator: http://{args.host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()