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
    def display_project_results(file_results: List[Dict[str, Any]]) -> None:
        """
        Display metrics for each file and also display aggregated project metrics.

        :param file_results: List of dictionaries with file metrics.
        :return: None.
        """
        for res in file_results:
            MetricsDisplay.display_metric_grid(res)
        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
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
        file_results = FileLoader.load_dataset(directory)
        ProjectAnalyzer.display_project_results(file_results)
        ProjectAnalyzer.export_to_csv(file_results, output_file)

# =============================================================================
# Main Routine
# =============================================================================
def main():
    """
    Main routine to analyze a directory of Python files and display the results.
    """
    import pandas as pd
    import os

    dataset_directory = FileLoader.get_dir_path("eval")
    file_results = FileLoader.load_dataset(dataset_directory)  # ← Load + analyze each file
    
    for result in file_results:
        print(f"{result['identifier']} → {result['doc_type']}")
    # Create exports folder if it doesn't exist
    os.makedirs("exports", exist_ok=True)

    # Convert file-level metrics
    df_file_metrics = pd.DataFrame(file_results)
    df_file_metrics["level"] = "file"

    # Convert project-level metrics
    project_metrics = ScoreAggregator.aggregate_project_score(file_results)
    df_project_metrics = pd.DataFrame([project_metrics])
    df_project_metrics["level"] = "project"

    # Combine both into one file
    combined_df = pd.concat([df_file_metrics, df_project_metrics], ignore_index=True)
    combined_df.to_csv("exports/all_metrics_combined.csv", index=False)




if __name__ == "__main__":
    main()
