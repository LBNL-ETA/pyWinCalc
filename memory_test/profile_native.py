"""Profile memory usage of a native executable (e.g. wincalc-test.exe)."""

import subprocess
import sys
from pathlib import Path

from profiler import collect_memory
from plotter import plot_memory

DEFAULT_EXE = Path(r"D:\WinCalc\cmake-build-release\bin\wincalc-test.exe")


def main():
    exe_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_EXE

    if not exe_path.exists():
        print(f"Executable not found: {exe_path}")
        sys.exit(1)

    print(f"Profiling: {exe_path}")
    proc = subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))

    output_dir = Path(__file__).resolve().parent
    csv_path = str(output_dir / "native_memory.csv")
    plot_path = str(output_dir / "native_memory.png")

    times, rss_values, vms_values = collect_memory(proc, csv_path)
    if times:
        plot_memory(times, rss_values, vms_values,
                    title=f"WinCalc Native Test — Memory Usage ({exe_path.name})",
                    output_path=plot_path)
    else:
        print("No memory samples collected.")


if __name__ == "__main__":
    main()
