import os
from typing import List, Dict, Any, Optional

from documetrics.CodeAnalyzer import CodeAnalyzer
from documetrics.globals import debug


class FileLoader:
    @staticmethod
    def load_single_file(file_path: str, throw: bool = False) -> Dict[str, Any] | None:
        """
        Load and analyze a single Python file.

        :param file_path: Path to the file.
        :param throw: If True, throw an exception if reading file causes an error
            If a file is within a folder, we just skip it rather than halting execution.
        :return: Dictionary with file metrics.
        :raises FileNotFoundError: If the file does not exist.
        :raises RunTimeError: If throw is true, and error reading file
        """
        if not os.path.exists(file_path): # should never happen
            print(f"File not found: {file_path}")
            raise FileNotFoundError
        metrics = CodeAnalyzer.analyze_file(file_path, throw)
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
        if os.path.isfile(directory):
            if debug: print(f"Analyzing file: {directory}")
            metrics = FileLoader.load_single_file(directory, throw=True)
            if metrics is None:  # This should not happen if throw=True
                raise RuntimeError(f"Unexpected error: No metrics returned for file {directory}")
            results.append(metrics)
            return results
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if debug: print(f"Analyzing file: {file_path}")
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
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        target_dir = base_dir if sub_folder_name is None else os.path.join(base_dir, sub_folder_name)

        if debug: print(f"Analyzing files in directory: {target_dir}")
        if not os.path.exists(target_dir):
            print(f"Directory not found: {base_dir}")
            raise FileNotFoundError
        return target_dir

    @staticmethod
    def find_common_path_prefix(paths: List[str]) -> str:
        normalized = [p.replace("\\", "/") for p in paths]
        prefix = os.path.commonprefix(normalized)
        if not prefix.endswith("/"):
            prefix = "/".join(prefix.split("/")[:-1]) + "/"
        return prefix

    @staticmethod
    def trim_common_path_in_identifiers(data: List[Dict[str, Any]]) -> None:
        # Extract all identifiers that are actual file paths
        paths = [
            d["identifier"].replace("\\", "/")
            for d in data
            if d.get("identifier") != "Project Results"
        ]

        if not paths:
            return

        common_prefix = FileLoader.find_common_path_prefix(paths)

        for d in data:
            if d.get("identifier") != "Project Results":
                normalized = d["identifier"].replace("\\", "/")
                if normalized.startswith(common_prefix):
                    d["identifier"] = normalized[len(common_prefix):]
                else:
                    d["identifier"] = normalized
