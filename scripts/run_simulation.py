"""python -m scripts.run_simulation --fail E28 E29 E38 --export output/trace.json"""
import argparse
from cases.scenario_loader import load_scenario
from config.settings import DEFAULT_SCENARIO
from core.simulation_runner import SimulationRunner
from core.simulation_observers import ConsoleObserver, JsonTraceObserver


def main():
    parser = argparse.ArgumentParser(description="Simulasi MST kumulatif dari dataset skenario.")
    parser.add_argument("--scenario", default=str(DEFAULT_SCENARIO))
    parser.add_argument("--fail", nargs="*", default=[])
    parser.add_argument("--export", help="Lokasi file JSON hasil dan trace.")
    args = parser.parse_args()
    observers = [ConsoleObserver()]
    if args.export:
        observers.append(JsonTraceObserver(args.export))
    runner = SimulationRunner(load_scenario(args.scenario), observers)
    if len(set(args.fail)) != len(args.fail) or set(args.fail) - runner.edge_ids:
        parser.error("Urutan kerusakan harus berisi ID edge unik yang tersedia.")
    runner.compute([])
    for iteration in range(1, len(args.fail) + 1):
        runner.compute(args.fail[:iteration])


if __name__ == "__main__":
    main()
