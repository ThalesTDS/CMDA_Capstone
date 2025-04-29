import os
from typing import List, Dict, Any
import pandas as pd

from .FileLoader import FileLoader
from .MetricsDisplay import MetricsDisplay
from .ScoreAggregator import ScoreAggregator

class ProjectAnalyzer:
    @staticmethod
    def analyze_and_export(input_directory: str, output_csv: str) -> list:
        """
        Analyze all Python files in a directory, export results to CSV, and collect any warnings.
        Returns:
            List of warning strings.
        """
        file_results = []
        warnings_list = []

        try:
            file_results = FileLoader.load_dataset(input_directory)
        except Exception as e:
            warnings_list.append(f"Failed to load dataset: {str(e)}")

        clean_results = []
        for result in file_results:
            if result is None:
                warnings_list.append(f"⚠️ Skipped a file (could not be processed).")
            else:
                clean_results.append(result)

        if not clean_results:
            warnings_list.append("⚠️ No files were successfully processed.")

        # Save results
        df_file_metrics = pd.DataFrame(clean_results)
        if not df_file_metrics.empty:
            df_file_metrics["level"] = "file"
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            df_file_metrics.to_csv(output_csv, index=False)

        return warnings_list

# =============================================================================
# No main() anymore because dashboard will call ProjectAnalyzer.analyze_and_export()
# =============================================================================
