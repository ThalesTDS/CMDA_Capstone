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
    def export_to_csv(file_results: List[Dict[str, Any]], project_results: Dict[str, Any]) -> None:
        """
        Export the analysis results to a CSV file.

        :param file_results: List of dictionaries with file metrics.
        :param project_results: Aggregated project metrics.
        :return: None.
        """
        output_file = os.path.join(os.path.dirname(__file__), "outputs", "all_metrics_combined.csv")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        for d in file_results:
            d["level"] = "file"
        project_results["level"] = "project"

        df = pd.DataFrame(file_results + [project_results])
        df.to_csv(output_file, index=False)

    @staticmethod
    def analyze_and_export(directory: str) -> None:
        """
        Analyze all Python files in a directory and display both individual and aggregated metrics.

        :param directory: Path to the directory containing Python files.
        :return: None.
        """
        file_results = FileLoader.load_dataset(directory)
        project_metrics = ScoreAggregator.aggregate_project_score(file_results)
        if debug: ProjectAnalyzer.print_results(file_results, project_metrics)
        FileLoader.trim_common_path_in_identifiers(file_results)
        ProjectAnalyzer.export_to_csv(file_results, project_metrics)

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
        # noinspection PyBroadException
        try:
            import torch
            torch.cuda.empty_cache()  # flush GPU allocator
            torch.cuda.synchronize()  # wait for kernels to finish
        except Exception:
            pass
        gc.collect()  # encourage finalizers

    @staticmethod
    def input_validation(file_path: str) -> Dict[str, int | str]:
        if not file_path: # Check for None or empty string
            return {"code": -1, "message": "No file or directory provided."}
        if not os.path.exists(file_path): # Check if path exists
            return {"code": -2, "message": f"Invalid file or directory path: {file_path}"}
        if not os.path.isfile(file_path) and not os.path.isdir(file_path): # Check if it's a file or directory
            return {"code": -3, "message": f"Path is neither a file nor a directory: {file_path}"}
        if os.path.isfile(file_path):
            if not file_path.endswith(".py"): # Check for Python file extension
                return {"code": -4, "message": f"File is not a Python (.py) file: {file_path}"}
            if os.path.getsize(file_path) == 0:  # Check for empty file
                return {"code": -5, "message": f"File is empty: {file_path}"}
        if os.path.isdir(file_path):
            py_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(file_path) for f in filenames if f.endswith(".py")]
            if not py_files:  # Check if directory contains Python files
                return {"code": -6, "message": f"Directory does not contain any Python (.py) files: {file_path}"}
        if not os.access(file_path, os.R_OK):  # Check for read permissions
            return {"code": -7, "message": f"Permission denied for file or directory: {file_path}"}
        return {"code": 0, "message": "Validation successful."}


    # =============================================================================
    # Main Routine
    # =============================================================================
    @staticmethod
    def main(file_path: str = None) -> Dict[str, int | str]:
        """
        Main routine to analyze a Python file or directory containing Python files.

        :param file_path: Path to a single Python file or directory. If None, error is raised.
        """
        validation_result = ProjectAnalyzer.input_validation(file_path)
        if validation_result["code"] != 0:
            return validation_result
        ProjectAnalyzer.analyze_and_export(file_path)
        ProjectAnalyzer.cleanup()
        return validation_result


if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    result = ProjectAnalyzer.main(user_input)
    print(result["message"])
