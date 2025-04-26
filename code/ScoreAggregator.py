from typing import List, Dict, Any
import numpy as np
from globals import METRICS_LIST


# =============================================================================
# Aggregate Scoring
# =============================================================================
class ScoreAggregator:
    # Global adjustable weights; must sum to 1.
    WEIGHTS: Dict[str, float] = {
        "comment_density": 0.3,
        "completeness": 0.4,
        "conciseness": 0.2,
        "accuracy": 0.1
    }

    @staticmethod
    def compute_file_score(metrics: Dict[str, float]) -> float:
        """
        Compute a weighted overall score for a single file based on individual metrics.

        :param metrics: Dictionary with keys corresponding to metric names (each normalized between 0 and 1).
        :return: Weighted overall score.
        :raises AssertionError: If the weights do not sum to 1.
        """
        assert np.isclose(sum(ScoreAggregator.WEIGHTS.values()), 1.0), "Weights must sum to 1"
        score = 0.0
        for key, weight in ScoreAggregator.WEIGHTS.items():
            if key in metrics:
                score += metrics[key] * weight
        return score

    @staticmethod
    def aggregate_project_score(file_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate metrics from multiple files into an overall project score weighted by line count.

        :param file_results: List of dictionaries where each contains file metrics and a 'line_count'.
        :return: Aggregated metrics dictionary.
        :raises ValueError: If the total line count is zero.
        """
        total_lines = sum(res.get("line_count", 0) for res in file_results)
        if total_lines == 0:
            raise ValueError("No lines found in the project.")

        if all(res["doc_type"] == "llm" for res in file_results):
            project_type = "LLM"
        elif all(res["doc_type"] == "Human" for res in file_results):
            project_type = "Human"
        else:
            project_type = "Mixed"

        aggregated_metrics: Dict[str, Any] = {
            "comment_density": 0.0,
            "completeness": 0.0,
            "conciseness": 0.0,
            "accuracy": 0.0,
            "overall_score": 0.0,
            "line_count": total_lines,
            "doc_type": project_type,
            "num_files": len(file_results),
            "identifier": "Project Results"
        }

        for res in file_results:
            for key in METRICS_LIST:
                aggregated_metrics[key] += res.get(key, 0) * res.get("line_count", 0)

        for key in aggregated_metrics:
            if key not in ["identifier", "line_count", "doc_type", "num_files"]:
                aggregated_metrics[key] /= total_lines

        return aggregated_metrics
