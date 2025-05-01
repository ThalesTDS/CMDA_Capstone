import os
from typing import List, Dict, Any
import pandas as pd

from .FileLoader import FileLoader
from .MetricsDisplay import MetricsDisplay
from .ScoreAggregator import ScoreAggregator



# =============================================================================
# File and Project Analysis
# =============================================================================

class ProjectAnalyzer:
    print("✅ Defining ProjectAnalyzer class")

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
            # MetricsDisplay.print_file_results(res)
        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
        if plot:
            MetricsDisplay.display_metric_grid(project_metrics)

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
        print("Step 1: Calling FileLoader.load_dataset()")
        file_results = FileLoader.load_dataset(directory)
        print("Step 2: Finished load_dataset")

        print("Step 3: Calling display_project_results()")
        ProjectAnalyzer.display_project_results(file_results)
        print("Step 4: Finished display_project_results")

        print("Step 5: Calling export_to_csv()")
        ProjectAnalyzer.export_to_csv(file_results, output_file)
        print("Step 6: Finished export_to_csv")

