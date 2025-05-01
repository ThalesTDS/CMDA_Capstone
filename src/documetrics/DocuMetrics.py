import os
from typing import List, Dict, Any

import pandas as pd

from documetrics.FileLoader import FileLoader 
from documetrics.MetricsDisplay import MetricsDisplay
from documetrics.ScoreAggregator import ScoreAggregator
from documetrics.globals import debug


# =============================================================================
# File and Project Analysis
# =============================================================================

class ProjectAnalyzer:
    @staticmethod
    def display_project_results(file_results: List[Dict[str, Any]], project_results: Dict[str, Any],
                                plot: bool = False) -> None:
        """
        Displays and prints metrics for each file and aggregated project metrics.

        :param file_results: List of dictionaries with file metrics.
        :param project_results: Aggregated project metrics.
        :param plot: If True, display the metrics in a grid format.
        :return: None.
        """
        if plot or debug:
            for res in file_results:
                if plot: MetricsDisplay.display_metric_grid(res)
                if debug: MetricsDisplay.print_file_results(res)
        if plot: MetricsDisplay.display_metric_grid(project_results)
        MetricsDisplay.print_file_results(project_results)

    @staticmethod
    def export_to_csv(file_results: List[Dict[str, Any]], project_results: Dict[str, Any], output_file: str) -> None:
        """
        Export the analysis results to a CSV file.

        :param file_results: List of dictionaries with file metrics.
        :param project_results: Aggregated project metrics.
        :param output_file: Path to the output CSV file.
        :return: None.
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        for d in file_results:
            d["level"] = "file"
        project_results["level"] = "project"

        df = pd.DataFrame(file_results + [project_results])
        df.to_csv(output_file, index=False)

    @staticmethod
    def analyze_and_export(directory: str, output_file: str = "outputs/all_metrics_combined.csv") -> None:
        """
        Analyze all Python files in a directory and display both individual and aggregated metrics.

        :param directory: Path to the directory containing Python files.
        :param output_file: Path to the output CSV file.
        :return: None.
        """
        file_results = FileLoader.load_dataset(directory)

        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
        ProjectAnalyzer.display_project_results(file_results, project_metrics)
        ProjectAnalyzer.export_to_csv(file_results, project_metrics, output_file)

    @staticmethod
    def cleanup() -> None:
        """
        Perform cleanup operations to release resources and terminate the program.

        - Closes all open matplotlib figures.
        - Clears the GPU memory cache using PyTorch.
        - Synchronizes GPU kernels to ensure all operations are complete.
        - Triggers garbage collection to finalize and free memory.
        - Exits the program to terminate any stray non-daemon threads.
        """
        import matplotlib.pyplot as plt, sys, gc
        plt.close('all')  # shut down any open figures
        try:
            import torch
            torch.cuda.empty_cache()  # flush GPU allocator
            torch.cuda.synchronize()  # wait for kernels to finish
        except Exception:
            pass
       
        gc.collect()  # encourage finalizers
        sys.exit(0)  # kill stray non-daemon threads


# =============================================================================
# Main Routine
# =============================================================================
def main():
    """
    Main routine to analyze a directory of Python files and display the results.
    """
    dataset_directory = FileLoader.get_dir_path()
    ProjectAnalyzer.analyze_and_export(dataset_directory)
    ProjectAnalyzer.cleanup()


if __name__ == "__main__":
    main()
