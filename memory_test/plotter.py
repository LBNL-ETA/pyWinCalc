import matplotlib.pyplot as plt


def plot_memory(times, rss_values, vms_values, title="Memory Usage", output_path="memory_plot.png"):
    """Plot RSS and VMS over time with peak annotation."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(times, rss_values, color="tab:blue", linewidth=0.8)
    axes[0].set_ylabel("RSS (MB)")
    axes[0].set_title("Resident Set Size (physical memory)")
    axes[0].grid(True, alpha=0.3)
    axes[0].fill_between(times, rss_values, alpha=0.15, color="tab:blue")

    axes[1].plot(times, vms_values, color="tab:orange", linewidth=0.8)
    axes[1].set_ylabel("VMS (MB)")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_title("Virtual Memory Size")
    axes[1].grid(True, alpha=0.3)
    axes[1].fill_between(times, vms_values, alpha=0.15, color="tab:orange")

    peak_rss = max(rss_values)
    peak_idx = rss_values.index(peak_rss)
    axes[0].annotate(
        f"Peak: {peak_rss:.1f} MB",
        xy=(times[peak_idx], peak_rss),
        xytext=(times[peak_idx], peak_rss * 1.05),
        arrowprops=dict(arrowstyle="->", color="red"),
        color="red",
        fontsize=9,
    )

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Memory plot saved to {output_path}")
    plt.show()
