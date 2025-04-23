import os
import re
import ast
import io
import tokenize
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Global metric list used for aggregation and display.
METRICS_LIST = [
    "comment_density",
    "completeness",
    "conciseness",
    "accuracy",
    "overall_score"
]

model = SentenceTransformer("all-MiniLM-L6-v2")
# =============================================================================
# Code Parsing & Extraction
# =============================================================================
class CodeParser:
    @staticmethod
    def extract_comments(code: str) -> Tuple[List[Tuple[int, str]], List[str]]:
        """
        Extract inline comments and docstrings from the provided source code.

        :param code: The source code as a string.
        :return: A tuple where the first element is a list of inline comments
                 (each as a tuple of line number and comment text) and the second
                 element is a list of docstring texts.
        """
        inline_comments = []
        try:
            tokens = tokenize.generate_tokens(io.StringIO(code).readline)
            for token in tokens:
                if token.type == tokenize.COMMENT:
                    inline_comments.append((token.start[0], token.string.strip()))
        except Exception as e:
            print("Tokenize error:", e)

        docstrings = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                    doc = ast.get_docstring(node)
                    if doc:
                        docstrings.append(doc)
        except Exception as e:
            print("AST error:", e)

        return inline_comments, docstrings

    @staticmethod
    def get_ast(code: str) -> Optional[ast.AST]:
        """
        Parse the source code into an Abstract Syntax Tree (AST).

        :param code: The source code as a string.
        :return: The AST object if parsing is successful; otherwise, None.
        """
        try:
            return ast.parse(code)
        except Exception as e:
            print("AST parsing error:", e)
            return None


# =============================================================================
# Metrics Calculation
# =============================================================================
class CodeMetrics:
    # Load a sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    @staticmethod
    def compute_comment_density(code: str,
                                inline_comments: List[Tuple[int, str]],
                                docstrings: List[str]) -> float:
        """
        Compute the normalized comment density of the source code.

        :param code: The source code as a string.
        :param inline_comments: List of tuples (line number, inline comment).
        :param docstrings: List of docstring texts.
        :return: Normalized comment density score between 0 and 1.
        """
        lines = code.splitlines()
        total_lines = sum(1 for line in lines if line.strip() != "")

        # Unique inline comment lines.
        comment_line_numbers = {line_no for line_no, _ in inline_comments}
        inline_comment_lines = len(comment_line_numbers)

        # Count docstring lines.
        docstring_lines = sum(len(doc.splitlines()) for doc in docstrings)
        total_comment_lines = inline_comment_lines + docstring_lines
        density = total_comment_lines / total_lines if total_lines > 0 else 0

        return CodeMetrics.normalize_comment_density(density)

    @staticmethod
    def normalize_comment_density(ratio: float,
                                  ideal_low: float = 0.1,
                                  ideal_high: float = 0.3,
                                  max_ratio: float = 1.0) -> float:
        """
        Normalize the comment density ratio into a quality score between 0 and 1.
        The ideal range is between `ideal_low` and `ideal_high`. Values outside the
        ideal range are scaled linearly.

        :param ratio: The computed comment density ratio.
        :param ideal_low: Lower bound of the ideal comment density.
        :param ideal_high: Upper bound of the ideal comment density.
        :param max_ratio: Maximum possible ratio (used to cap the scaling).
        :return: Normalized quality score between 0 and 1.
        """
        if ideal_low <= ratio <= ideal_high:
            return 1.0
        elif ratio < ideal_low:
            return ratio / ideal_low
        else:  # ratio > ideal_high
            if ratio >= max_ratio:
                return 0.0
            else:
                return (max_ratio - ratio) / (max_ratio - ideal_high)

    @staticmethod
    def compute_completeness(code: str, docstring: str) -> float:
        """
        Check if the docstring contains required elements based on function/class definition.

        :param code: The full source code containing the function/class.
        :param docstring: The function/class docstring.
        :return: A completeness score between 0 (incomplete) and 1 (fully complete).
        """
        if not docstring:
            return 0.0

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):  # Check function definitions
                    param_names = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]
                    has_return = isinstance(node.returns, ast.Name)  # Checks if a return type is declared

                    needs_param = len(param_names) > 0  # Function requires @param if it has parameters
                    needs_return = has_return  # Function requires @return if return type exists

                    # Check if the docstring contains necessary components
                    has_param_doc = all(
                        f"@param {param}" in docstring for param in param_names) if needs_param else True
                    has_return_doc = "@return" in docstring if needs_return else True
                    has_general_desc = len(
                        docstring.strip().split("\n")[0].split()) > 5  # At least 5 words in first line

                    # Calculate completeness score
                    completeness_score = 0.0
                    if has_general_desc:
                        completeness_score += 0.5  # General description contributes 50%
                    if needs_param and has_param_doc:
                        completeness_score += 0.25  # Parameter documentation is 25%
                    if needs_return and has_return_doc:
                        completeness_score += 0.25  # Return documentation is 25%

                        # Check if the docstring contains a general description (not just `@param` and `@return`)
                        docstring_lines = docstring.strip().split("\n")
                        first_line = docstring_lines[0].strip() if docstring_lines else ""
                        has_general_description = len(first_line.split()) > 5  # Requires at least 5 words

                        # Calculate completeness score
                        completeness_score = 0.0
                        if has_general_description:
                            completeness_score += 0.4  # General description carries 40% weight
                        if needs_param and "@param" in docstring:
                            completeness_score += 0.3  # Params contribute 30% to completeness
                        if needs_return and "@return" in docstring:
                            completeness_score += 0.3  # Return doc contributes 30%

                        return completeness_score
        except SyntaxError:
            return 0.0  # Fallback in case of syntax issues

        return 1.0  # Default case (should never reach here)

    @staticmethod
    def compute_similarity(text1: str, text2: str) -> float:
        """
        Compute the cosine similarity between two texts using TF-IDF.

        :param text1: The first text string.
        :param text2: The second text string.
        :return: Cosine similarity score between 0 and 1. Returns 0 if either text is empty.
        """
        if not text1.strip() or not text2.strip():
            return 0.0
        try:
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([text1, text2])
            sim_matrix = cosine_similarity(vectors)
            return sim_matrix[0, 1]
        except ValueError:
            return 0.0

    @staticmethod
    def compute_conciseness(comments: List[str], verbose_threshold: int = 20, similarity_threshold: float = .70) -> float:
        """
        Detect how concise comments are using similarity and wordy sentences. Sentences are considered wordy if they
        pass a designated threshold and the same follows for similarity. By default, verbose threshold is 20 words in a sentence,
        and similarity is .50. If the score is high, then conciseness is worse and vice versa. Therefore, we compute the conciseness by
        dividing our weighted score with a maximum score. We subtract it from 1. This way, we have a score between 0 and 1, with a lower score
        being a worse level of conciseness

        :param comments: List of comment strings.
        :param verbose_threshold: Word count threshold to consider a comment as verbose.
        :return: Score between 0 and 1 where 1 means all comments are concise.
        """
        embeddings = model.encode(comments)
        similarities = model.similarity(embeddings, embeddings).numpy() # since similarity() returns a tensor object, we want a 2D array for simplicity
        
        """
            This algorithm is a bit tricky to understand, but I will walk you through. Our similarity scores is a tensor matrix. To simplify
            its usage, I turned it into a numpy array that 2-D. Since we have n sentences, our matrix is n by n. To check if each sentence
            passes our similarity and verbose threshold, I iterate through a row, with our anchor sentence being the col at the same index
            as row. So, if are are row 0, then we start from col 0. If we are at row 3, we iterate through the row starting at col 3. Initially
            we set our anchor before the loop to make things easier. If each similarity score is above our threshold, we have only gone
            through the first row and are done. If a sentence is below the threshold, we use that sentence as the new anchor point by moving
            to its corresponding index within the column. Then, we start from that index and continue iterating through the columns

        """
        ncols = len(similarities) # our 2D array is a square matrix, so we only need length of one dimension
        row = 0
        
        verbose_count = 0
        if len(comments[0]) > verbose_threshold:
            verbose_count = 1

        
        similar_count = 0
        for col in range(1, ncols):
            
            if similarities[row, col] >= similarity_threshold:
                similar_count += 1
                
            else:
                row = col # move to the next anchor sentence's row index
            if len(comments[col]) > verbose_threshold:
                verbose_count += 1
                
        
        score = .75*verbose_count + .25*similar_count
        
        dim = len(comments) * len(comments)
        
        return 1 - (score / dim)

    @staticmethod
    def evaluate_accuracy(comment: str, code_snippet: str) -> float:
        """
        Evaluate the relevance of a comment by comparing its semantic similarity to the corresponding code snippet.
        Uses a pre-trained BERT-based model (Sentence-BERT) to compute similarity scores.

        :param comment: The comment text.
        :param code_snippet: The corresponding code line.
        :return: The cosine similarity score (between 0 and 1).
        """
        comment_embedding = CodeMetrics.model.encode(comment, convert_to_tensor=True)
        code_embedding = CodeMetrics.model.encode(code_snippet, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(comment_embedding, code_embedding)
        return similarity.item()

    @staticmethod
    def compute_accuracy_scores(inline_comments: List[Tuple[int, str]], code_lines: List[str]) -> float:
        accuracy_scores = []
        for line_no, comment in inline_comments:
            if 1 <= line_no <= len(code_lines):
                code_line = code_lines[line_no - 1]
                accuracy_scores.append(CodeMetrics.evaluate_accuracy(comment, code_line))
        return np.mean(accuracy_scores) if accuracy_scores else 0.0


# =============================================================================
# Aggregate Scoring
# =============================================================================
class ScoreAggregator:
    # Global adjustable weights; must sum to 1.
    WEIGHTS: Dict[str, float] = {
        "comment_density": 1 / 4,
        "completeness": 1 / 4,
        "conciseness": 1 / 4,
        "accuracy": 1 / 4
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


# =============================================================================
# Display Functions
# =============================================================================
class MetricsDisplay:
    @staticmethod
    def display_metric_grid(metrics: Dict[str, Any]) -> None:
        """
        Display individual metric boxes and a large box for the overall score in a grid format.
        Uses a color map (green = good, red = bad) based on normalized values.

        :param metrics: Dictionary containing metric values and metadata.
        :return: None.
        """
        extras = {"line_count", "identifier", "doc_type", "num_files"}
        all_metrics = {k: float(v) for k, v in metrics.items() if k not in extras}

        # Separate overall score from individual metrics.
        overall_score = all_metrics.pop("overall_score", None)
        assert overall_score is not None, "Overall score must be computed."

        metric_keys = list(all_metrics.keys())

        fig = plt.figure(figsize=(6, 9))
        gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 0.6])
        cmap = plt.get_cmap("RdYlGn")

        for i, key in enumerate(metric_keys):
            row = i // 2
            col = i % 2
            ax = fig.add_subplot(gs[row, col])
            val = all_metrics[key]
            color = cmap(val)
            ax.set_facecolor(color)
            ax.text(0.5, 0.5, f"{val:.2f}", fontsize=16, ha="center", va="center", weight="bold")
            ax.text(0.5, 0.1, key, fontsize=12, ha="center", va="center")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

        # Overall score spanning all columns.
        ax_score = fig.add_subplot(gs[2, :])
        color = cmap(overall_score)
        ax_score.set_facecolor(color)
        ax_score.text(0.5, 0.5, f"Overall: {overall_score:.2f}", fontsize=20, ha="center", va="center", weight="bold")
        ax_score.set_xticks([])
        ax_score.set_yticks([])
        for spine in ax_score.spines.values():
            spine.set_visible(False)

        plt.suptitle(f"{metrics['identifier']} ({metrics['doc_type']})", fontsize=16)
        plt.tight_layout(rect=(0, 0, 1, 0.95))
        plt.show()

        print("Filename:", metrics["identifier"])
        for metric in METRICS_LIST:
            print(f"{metric}: {metrics[metric]:.3f}")
        if metrics["identifier"] == "Project Results":
            print(f"Total lines: {metrics['line_count']}")
            print(f"Number of files: {metrics['num_files']}")
        print()


# =============================================================================
# File and Project Analysis
# =============================================================================
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
        return CodeAnalyzer.analyze_code(code, identifier=FileLoader.trim_file_path(file_path))


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
    def trim_file_path(file_path: str) -> str:
        """
        Trim the file path to begin from the 'data/' directory if present.

        :param file_path: Original file path.
        :return: Trimmed file path.
        """
        normalized_path = file_path.replace("\\", "/")
        match = re.search(r'data/.*', normalized_path)
        return match.group(0) if match else file_path

    @staticmethod
    def get_dir_path(sub_folder_name: Optional[str] = None) -> str:
        """
        Construct a directory path to the data folder or a subfolder within it.

        :param sub_folder_name: Optional data subfolder; if None, entire data directory is used.
        :return: Constructed path as a string.
        """
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        return base_dir if sub_folder_name is None else os.path.join(base_dir, sub_folder_name)


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
