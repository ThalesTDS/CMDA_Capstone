import re
from typing import Dict, Any

from documetrics.CodeMetrics import CodeMetrics
from documetrics.CodeParser import CodeParser
from documetrics.ScoreAggregator import ScoreAggregator


class CodeAnalyzer:
    @staticmethod
    def analyze_code(code: str, identifier: str = "unknown") -> Dict[str, Any] | None:
        """
        Analyze a code snippet and compute various metrics.

        :param code: The source code as a string.
        :param identifier: An identifier for the code snippet (e.g., filename).
        :return: Dictionary with computed metrics and metadata, or None if file does not contain
        enough comments or docstrings to be evaluated.
        """
        code_lines = [ln for ln in code.splitlines() if ln.strip()]  # no blanks

        if not code_lines:
            # empty file early drop out optimization
            return None
        docstrings = CodeParser.extract_comments(code)

        # As of now we require 1 docstring to be present in the code to be evaluated
        if not docstrings:
            print(f"File {identifier} does not contain enough docstrings to be evaluated.")
            return None

        density = CodeMetrics.compute_comment_density(code_lines)
        completeness = CodeMetrics.compute_completeness(code)
        conciseness = CodeMetrics.compute_conciseness(docstrings)
        accuracy = CodeMetrics.compute_accuracy_scores(code)

        metrics: Dict[str, Any] = {
            "comment_density": density,
            "completeness": completeness,
            "conciseness": conciseness,
            "accuracy": accuracy,
            "line_count": len(code_lines),
            "identifier": identifier,
        }

        metrics["overall_score"] = ScoreAggregator.compute_file_score(metrics)
        return metrics

    @staticmethod
    def analyze_file(file_path: str, throw: bool) -> Dict[str, Any] | None:
        """
        Load a Python file and analyze its code to compute metrics.

        :param file_path: Path to the Python file.
        :param throw: Throws an error if there is an error reading the file.
        :return: Dictionary with computed metrics, or None if reading fails.
        """
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                code = f.read()
        except Exception as e:
            if throw:
                raise RuntimeError(f"Error reading {file_path}: {e}")
            print(f"Error reading {file_path}: {e}")
            return None
        return CodeAnalyzer.analyze_code(code, identifier=file_path)
