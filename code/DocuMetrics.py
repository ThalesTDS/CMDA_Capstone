from typing import List, Dict, Any

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
    def analyze_directory(directory: str) -> None:
        """
        Analyze all Python files in a directory and display both individual and aggregated metrics.

        :param directory: Path to the directory containing Python files.
        :return: None.
        """
        file_results = FileLoader.load_dataset(directory)
        ProjectAnalyzer.display_project_results(file_results)


# =============================================================================
# Main Routine
# =============================================================================
def main():
    """
    Main routine to analyze a directory of Python files and display the results.
    """
    dataset_directory = FileLoader.get_dir_path()
    ProjectAnalyzer.analyze_directory(dataset_directory)


if __name__ == "__main__":
    main()
