import os
from typing import List, Dict, Any, Optional

from CodeAnalyzer import CodeAnalyzer


class FileLoader:
    @staticmethod
    def load_single_file(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load and analyze a single Python file.

        :param file_path: Path to the file.
        :return: Dictionary with file metrics.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            raise FileNotFoundError
        metrics = CodeAnalyzer.analyze_file(file_path)
        if metrics is not None:
            label = "LLM" if "llm" in file_path.lower() else "Human"
            metrics["doc_type"] = label
        return metrics

    @staticmethod
    def load_dataset(directory: str) -> List[Dict[str, Any]]:
        """
        Walk through a directory to analyze all .py files and collect their metrics.

        :param directory: Directory path containing Python files.
        :return: List of dictionaries with file metrics.
        """
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    metrics = FileLoader.load_single_file(file_path)
                    if metrics is not None:
                        results.append(metrics)
        return results

    @staticmethod
    def get_dir_path(sub_folder_name: Optional[str] = None) -> str:
        """
        Construct a directory path to the data folder or a subfolder within it.

        :param sub_folder_name: Optional data subfolder; if None, entire data directory is used.
        :return: Constructed path as a string.
        """
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        return base_dir if sub_folder_name is None else os.path.join(base_dir, sub_folder_name)
