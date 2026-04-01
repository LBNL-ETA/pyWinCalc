"""Profile memory usage while running the pywincalc pytest suite."""

import subprocess
import sys
from pathlib import Path

from profiler import collect_memory
from plotter import plot_memory

REPO_ROOT = Path(__file__).resolve().parent.parent


def main():
    proc = subprocess.Popen(
        [sys.executable, "-m", "pytest", "-ra", "-vv", "test/"],
        cwd=str(REPO_ROOT),
    )

    csv_path = str(REPO_ROOT / "memory_test" / "pytest_memory.csv")
    plot_path = str(REPO_ROOT / "memory_test" / "pytest_memory.png")

    times, rss_values, vms_values = collect_memory(proc, csv_path)
    if times:
        plot_memory(times, rss_values, vms_values,
                    title="pywincalc Test Suite — Memory Usage",
                    output_path=plot_path)
    else:
        print("No memory samples collected.")


if __name__ == "__main__":
    main()
