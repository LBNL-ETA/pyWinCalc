import psutil
import time
import csv


def get_total_memory(parent):
    """Sum memory across the process and all its children."""
    total_rss = 0
    total_vms = 0
    try:
        mem = parent.memory_info()
        total_rss += mem.rss
        total_vms += mem.vms
        for child in parent.children(recursive=True):
            try:
                cmem = child.memory_info()
                total_rss += cmem.rss
                total_vms += cmem.vms
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return total_rss, total_vms


def collect_memory(proc, csv_path="memory_log.csv"):
    """Poll memory of a running subprocess and its children every 10ms."""
    psproc = psutil.Process(proc.pid)

    times = []
    rss_values = []
    vms_values = []

    with open(csv_path, "w", newline="") as log:
        writer = csv.writer(log)
        writer.writerow(["time_s", "rss_mb", "vms_mb"])
        start = time.perf_counter()

        while proc.poll() is None:
            try:
                total_rss, total_vms = get_total_memory(psproc)
                elapsed = time.perf_counter() - start
                rss_mb = total_rss / 1024 / 1024
                vms_mb = total_vms / 1024 / 1024

                writer.writerow([
                    f"{elapsed:.3f}",
                    f"{rss_mb:.2f}",
                    f"{vms_mb:.2f}",
                ])

                times.append(elapsed)
                rss_values.append(rss_mb)
                vms_values.append(vms_mb)
            except psutil.NoSuchProcess:
                break
            time.sleep(0.01)

    print(f"\nProcess exit code: {proc.returncode}")
    print(f"Memory log saved to {csv_path}")

    return times, rss_values, vms_values
