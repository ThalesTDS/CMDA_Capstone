from typing import Dict, Any, Optional
from CodeParser import CodeParser
from CodeMetrics import CodeMetrics
from ScoreAggregator import ScoreAggregator
from globals import trim_file_path


class CodeAnalyzer:
    @staticmethod
    def analyze_code(code: str, identifier: str = "unknown") -> Dict[str, Any]:
        """
        Analyze a code snippet and compute various metrics.

        :param code: The source code as a string.
        :param identifier: An identifier for the code snippet (e.g., filename).
        :return: Dictionary with computed metrics and metadata.
        """
        code_lines = code.splitlines()
        inline_comments, docstrings = CodeParser.extract_comments(code)
        all_comments = [comment for _, comment in inline_comments] + docstrings

        density = CodeMetrics.compute_comment_density(code, inline_comments, docstrings)
        docstring = docstrings[0] if docstrings else ""

        completeness = CodeMetrics.compute_completeness(code, docstring)
        conciseness = CodeMetrics.compute_conciseness(all_comments)
        accuracy = CodeMetrics.compute_accuracy_scores(inline_comments, code_lines)

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
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        return CodeAnalyzer.analyze_code(code, identifier=trim_file_path(file_path))
