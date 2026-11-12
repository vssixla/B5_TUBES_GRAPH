# Konfigurasi untuk website, runner CLI, dan benchmark
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "static"
SCENARIOS_DIR = ROOT / "cases" / "scenarios"
DEFAULT_SCENARIO = SCENARIOS_DIR / "case_26_gudang_terbakar" / "scenario.json"
DEFAULT_PORT = 8000
BENCHMARK_ROUNDS = 15
BENCHMARK_BATCH_SIZE = 30
WARMUP_RUNS = 3