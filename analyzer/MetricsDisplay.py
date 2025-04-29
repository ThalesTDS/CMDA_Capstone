from typing import Dict, Any, Union
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from .globals import METRICS_LIST


# =============================================================================
# Display Functions
# =============================================================================
class MetricsDisplay:
    @staticmethod
    def display_metric_grid(metrics: Dict[str, Any]) -> None:
        """
        Display individual metric boxes and a large box for the overall score in a grid format.
        Uses a color map (green = good, red = bad) based on normalized values.

        :param metrics: Dictionary containing metric values and metadata.
        :return: None.
        """
        extras = {"line_count", "identifier", "doc_type", "num_files"}
        all_metrics = {k: float(v) for k, v in metrics.items() if k not in extras}

        # Separate overall score from individual metrics.
        overall_score = all_metrics.pop("overall_score", None)
        assert overall_score is not None, "Overall score must be computed."

        metric_keys = list(all_metrics.keys())

        fig = plt.figure(figsize=(6, 9))
        gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 0.6])
        cmap = plt.get_cmap("RdYlGn")

        for i, key in enumerate(metric_keys):
            row = i // 2
            col = i % 2
            ax = fig.add_subplot(gs[row, col])
            val = all_metrics[key]
            color = cmap(val)
            ax.set_facecolor(color)
            ax.text(0.5, 0.5, f"{val:.2f}", fontsize=16, ha="center", va="center", weight="bold")
            ax.text(0.5, 0.1, key, fontsize=12, ha="center", va="center")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

        # Overall score spanning all columns.
        ax_score = fig.add_subplot(gs[2, :])
        color = cmap(overall_score)
        ax_score.set_facecolor(color)
        ax_score.text(0.5, 0.5, f"Overall: {overall_score:.2f}", fontsize=20, ha="center", va="center", weight="bold")
        ax_score.set_xticks([])
        ax_score.set_yticks([])
        for spine in ax_score.spines.values():
            spine.set_visible(False)

        plt.suptitle(f"{metrics['identifier']} ({metrics['doc_type']})", fontsize=16)
        plt.tight_layout(rect=(0, 0, 1, 0.95))
        plt.show()

        print("Filename:", metrics["identifier"])
        for metric in METRICS_LIST:
            print(f"{metric}: {metrics[metric]:.3f}")
        if metrics["identifier"] == "Project Results":
            print(f"Total lines: {metrics['line_count']}")
            print(f"Number of files: {metrics['num_files']}")
        print()
