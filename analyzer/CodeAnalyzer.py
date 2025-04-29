from typing import Dict, Any, Optional, Union
from .CodeParser import CodeParser
from .CodeMetrics import CodeMetrics
from .ScoreAggregator import ScoreAggregator
from .globals import trim_file_path


class CodeAnalyzer:
    @staticmethod
    def analyze_code(code: str, identifier: str = "unknown") -> Union[Dict[str, Any], None]:
        """
        Analyze a code snippet and compute various metrics.

        :param code: The source code as a string.
        :param identifier: An identifier for the code snippet (e.g., filename).
        :return: Dictionary with computed metrics and metadata, or None if file does not contain
        enough comments or docstrings to be evaluated.
        """
        code_lines = code.splitlines()
        # empty file early drop out optimization
        if not code_lines:
            return None
        inline_comments, docstrings, counts = CodeParser.extract_comments(code)

        # As of now we require 4 comments and 2 docstrings to be present in the code to be evaluated
        # TODO: Maybe make this a more useful output, possibly with a notice idk
        count_comments, count_docstrings = counts
        if count_comments < 2 or count_docstrings < 1:
            return None

        density = CodeMetrics.compute_comment_density(code_lines)
        completeness = CodeMetrics.compute_completeness(code)
        conciseness = CodeMetrics.compute_conciseness(docstrings)
        accuracy = CodeMetrics.compute_accuracy_scores(code)

        line_count = sum(1 for line in code_lines if line.strip())

        metrics: Dict[str, Any] = {
            "comment_density": density,
            "completeness": completeness,
            "conciseness": conciseness,
            "accuracy": accuracy
        }

        score = ScoreAggregator.compute_file_score(metrics)
        metrics["overall_score"] = score
        metrics["line_count"] = line_count
        metrics["identifier"] = identifier
        return metrics

    @staticmethod
    def analyze_file(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a Python file and analyze its code to compute metrics.

        :param file_path: Path to the Python file.
        :return: Dictionary with computed metrics, or None if reading fails.
        """
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        return CodeAnalyzer.analyze_code(code, identifier=trim_file_path(file_path))
