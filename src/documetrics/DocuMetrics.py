import os
from typing import List, Dict, Any

import pandas as pd

from documetrics.FileLoader import FileLoader
from documetrics.ScoreAggregator import ScoreAggregator
from documetrics.globals import debug, METRICS_LIST


# =============================================================================
# File and Project Analysis
# =============================================================================

class ProjectAnalyzer:
    @staticmethod
    def print_results(file_results: List[Dict[str, Any]], project_results: Dict[str, Any]) -> None:
        """
        Prints metrics for each file and aggregated project metrics.
        For debugging only.

        :param file_results: List of dictionaries with file metrics.
        :param project_results: Aggregated project metrics.
        :return: None.
        """

        def print_file_results(results: Dict[str, Any]) -> None:
            """
            Print the results of the analysis for each file.

            :param results: Dictionary containing file metrics.
            :return: None.
            """
            print("Filename:", results["identifier"])
            for metric in METRICS_LIST:
                print(f"{metric}: {results[metric]:.3f}")
            if results["identifier"] == "Project Results":
                print(f"Total lines: {results['line_count']}")
                print(f"Number of files: {results['num_files']}")
            print()

        for res in file_results:
            print_file_results(res)
        print_file_results(project_results)

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
        if debug: ProjectAnalyzer.print_results(file_results, project_metrics)
        ProjectAnalyzer.export_to_csv(file_results, project_metrics, output_file)

    @staticmethod
    def cleanup() -> None:
        """
        Perform cleanup operations to release resources and terminate the program.

        - Clears the GPU memory cache using PyTorch.
        - Synchronizes GPU kernels to ensure all operations are complete.
        - Triggers garbage collection to finalize and free memory.
        - Exits the program to terminate any stray non-daemon threads.
        """
        import sys, gc
        try:
            import torch
            torch.cuda.empty_cache()  # flush GPU allocator
            torch.cuda.synchronize()  # wait for kernels to finish
        except ImportError:
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
    dataset_directory = FileLoader.get_dir_path("working_pwc_code")
    ProjectAnalyzer.analyze_and_export(dataset_directory)
    ProjectAnalyzer.cleanup()


if __name__ == "__main__":
    main()
