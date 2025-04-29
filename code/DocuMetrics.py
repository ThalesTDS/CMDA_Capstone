import os
from typing import List, Dict, Any

import pandas as pd

from FileLoader import FileLoader
from MetricsDisplay import MetricsDisplay
from ScoreAggregator import ScoreAggregator


# =============================================================================
# File and Project Analysis
# =============================================================================

class ProjectAnalyzer:
    @staticmethod
    def display_project_results(file_results: List[Dict[str, Any]], plot: bool = False) -> None:
        """
        Displays and prints metrics for each file and also display aggregated project metrics.

        :param file_results: List of dictionaries with file metrics.
        :param plot: If True, display the metrics in a grid format.
        :return: None.
        """
        for res in file_results:
            if plot:
                MetricsDisplay.display_metric_grid(res)
            MetricsDisplay.print_file_results(res)
        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
        if plot:
            MetricsDisplay.display_metric_grid(project_metrics)
        MetricsDisplay.print_file_results(project_metrics)

    @staticmethod
    def export_to_csv(file_results: List[Dict[str, Any]], output_file: str) -> None:
        """
        Export the analysis results to a CSV file.

        :param file_results: List of dictionaries with file metrics.
        :param output_file: Path to the output CSV file.
        :return: None.
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        df_file_metrics = pd.DataFrame(file_results)
        df_file_metrics["level"] = "file"

        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
        df_project_metrics = pd.DataFrame([project_metrics])
        df_project_metrics["level"] = "project"

        combined_df = pd.concat([df_file_metrics, df_project_metrics], ignore_index=True)
        combined_df.to_csv(output_file, index=False)

    @staticmethod
    def analyze_and_export(directory: str, output_file: str = "exports/all_metrics_combined.csv") -> None:
        """
        Analyze all Python files in a directory and display both individual and aggregated metrics.

        :param directory: Path to the directory containing Python files.
        :param output_file: Path to the output CSV file.
        :return: None.
        """
        file_results = FileLoader.load_dataset(directory)
        ProjectAnalyzer.display_project_results(file_results)
        ProjectAnalyzer.export_to_csv(file_results, output_file)

    @staticmethod
    def cleanup():
        """
        Perform cleanup operations to release resources and terminate the program.

        - Closes all open matplotlib figures.
        - Clears the GPU memory cache using PyTorch.
        - Synchronizes GPU kernels to ensure all operations are complete.
        - Triggers garbage collection to finalize and free memory.
        - Exits the program to terminate any stray non-daemon threads.
        """
        import torch, matplotlib.pyplot as plt, sys, gc
        plt.close('all')  # shut down any open figures
        torch.cuda.empty_cache()  # flush GPU allocator
        torch.cuda.synchronize()  # wait for kernels to finish
        gc.collect()  # encourage finalizers
        sys.exit(0)  # kill stray non-daemon threads


# =============================================================================
# Main Routine
# =============================================================================
def main():
    """
    Main routine to analyze a directory of Python files and display the results.
    """
    dataset_directory = FileLoader.get_dir_path("working_pwc_code")
    ProjectAnalyzer.analyze_and_export(dataset_directory)
    ProjectAnalyzer.cleanup()


if __name__ == "__main__":
    main()
