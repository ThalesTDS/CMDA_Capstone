import os
import re
import ast
import io
import tokenize
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from textstat import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------
# 1. Metrics Section
# ---------------------------

def extract_comments(code):
    """
    Extract inline comments using tokenize and docstrings using ast.
    Returns a list of inline comments (with line numbers) and a list of docstrings.
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


def compute_comment_density(code, inline_comments, docstrings):
    """
    Compute the ratio of comment lines (inline and docstrings) to total non-blank lines.
    """
    lines = code.splitlines()
    total_lines = sum(1 for line in lines if line.strip() != "")

    # Count unique inline comment lines.
    comment_line_numbers = {line_no for line_no, _ in inline_comments}
    inline_comment_lines = len(comment_line_numbers)

    # Count docstring lines (using the number of lines in each docstring).
    docstring_lines = sum(len(doc.splitlines()) for doc in docstrings)
    total_comment_lines = inline_comment_lines + docstring_lines
    density = total_comment_lines / total_lines if total_lines > 0 else 0
    return normalize_comment_density(density)


def normalize_comment_density(ratio, ideal_low=0.1, ideal_high=0.3, max_ratio=1.0):
    """
    Normalize the comment density ratio into a quality score between 0 and 1.
    The ideal ratio is between `ideal_low` and `ideal_high`. Values within that range score 1.
    Below or above that range, the score falls off linearly.
    """
    if ideal_low <= ratio <= ideal_high:
        return 1.0
    elif ratio < ideal_low:
        return ratio / ideal_low  # linear scaling below the ideal range
    else:  # ratio > ideal_high
        if ratio >= max_ratio:  # more comments than code
            return 0
        else:
            return (max_ratio - ratio) / (max_ratio - ideal_high)


def compute_readability_scores(comments):
    """
    Compute the average normalized Flesch Reading Ease score for a list of comment strings.
    """
    scores = []
    for comment in comments:
        score = textstat.flesch_reading_ease(comment)
        scores.append(score)

    if scores:
        avg_score = np.mean(scores)
        # Normalize to range [0,1] where 0 = unreadable, 1 = very easy to read
        normalized_score = np.clip(avg_score / 100, 0, 1)  # Normalize and clip
        return normalized_score
    return 0  # Default to 0 if no comments


def check_completeness(code):
    """
    Check that all functions and classes have docstrings.
    Returns the ratio of documented definitions to the total definitions.
    """
    try:
        tree = ast.parse(code)
        nodes = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        total = len(nodes)
        documented = 0
        for node in nodes:
            doc = ast.get_docstring(node)
            if doc and len(doc.strip()) > 10:
                documented += 1
        return documented / total if total > 0 else 1
    except Exception:
        return 0


def compute_similarity(text1, text2):
    """
    Compute cosine similarity between two texts using TF-IDF.
    If either text is empty or an error occurs (e.g. empty vocabulary), returns 0.
    """
    if not text1.strip() or not text2.strip():
        return 0
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])
        sim_matrix = cosine_similarity(vectors)
        return sim_matrix[0, 1]
    except ValueError:
        # This catches errors like an empty vocabulary.
        return 0


def compute_redundancy(inline_comments, code_lines):
    """
    For each inline comment, compare it with its corresponding code line using cosine similarity.
    Returns the average similarity score.
    """
    similarities = []
    for line_no, comment in inline_comments:
        if 1 <= line_no <= len(code_lines):
            code_line = code_lines[line_no - 1]
            sim = compute_similarity(comment, code_line)
            similarities.append(sim)
    # For redundancy, a lower value is better. We invert the average similarity.
    avg_sim = np.mean(similarities) if similarities else 0
    return 1 - avg_sim


def check_conciseness(comments, verbose_threshold=20):
    """
    Detect overly verbose comments by computing the percentage of comments with a word count
    above the provided threshold.
    """
    verbose_count = 0
    for comment in comments:
        if len(comment.split()) > verbose_threshold:
            verbose_count += 1
    return 1 - (verbose_count / len(comments)) if comments else 1


def evaluate_accuracy(comment, code_snippet):
    """
    A heuristic to evaluate if the comment is relevant: computes the ratio of identifier tokens
    overlapping between the comment and the corresponding code snippet.
    """
    code_tokens = set(re.findall(r'\b\w+\b', code_snippet))
    comment_tokens = set(re.findall(r'\b\w+\b', comment))
    if not code_tokens:
        return 0
    overlap = code_tokens.intersection(comment_tokens)
    return len(overlap) / len(code_tokens)


# ---------------------------
# 2. Aggregate Weighting Section
# ---------------------------
# Global adjustable weights
WEIGHTS = {
    "comment_density": 1 / 6,
    "readability": 1 / 6,
    "completeness": 1 / 6,
    "redundancy": 1 / 6,
    "conciseness": 1 / 6,
    "accuracy": 1 / 6
}
METRICS_LIST = [
    "comment_density",
    "readability",
    "completeness",
    "redundancy",
    "conciseness",
    "accuracy",
    "overall_score"
]


def compute_file_score(metrics):
    """
    Compute a weighted score from individual metric values.
    It is assumed that each metric is normalized between 0 and 1.
    """
    assert sum(WEIGHTS.values()) == 1.0, "Weights must sum to 1"
    score = 0
    for key, weight in WEIGHTS.items():
        if key in metrics:
            score += metrics[key] * weight
    return score


def aggregate_project_score(file_results):
    """
    Given a list of file metric dictionaries (each with a 'score' and 'line_count'),
    compute the overall project score weighted by line count.
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

    aggregated_metrics = {
        "comment_density": 0,
        "readability": 0,
        "completeness": 0,
        "redundancy": 0,
        "conciseness": 0,
        "accuracy": 0,
        "overall_score": 0,
        "line_count": total_lines,
        "doc_type": project_type,
        "num_files": len(file_results),
        "identifier": "Project Results"
    }

    for res in file_results:
        for key in METRICS_LIST:
            aggregated_metrics[key] += res.get(key, 0) * res.get("line_count", 0)

    for key in aggregated_metrics:
        if key != "identifier" and key != "line_count" and key != "doc_type" and key != "num_files":
            aggregated_metrics[key] /= total_lines

    return aggregated_metrics


# ---------------------------
# 3. Improved Display Section
# ---------------------------
def display_metric_grid(metrics):
    """
    Display individual metric boxes plus one large box for the overall score.
    The metric values are assumed normalized in [0,1]. Their value is used directly to pick a color
    from the 'RdYlGn' colormap (green = good, red = bad).
    """
    # Remove keys that we don't want to show in the grid.
    extras = {"line_count", "identifier", "doc_type", "num_files"}
    all_metrics = {k: float(v) for k, v in metrics.items() if k not in extras}

    # Separate overall score if present.
    overall_score = all_metrics.pop("overall_score", None)
    # The remaining keys are the individual metrics (e.g., comment_density, readability, etc.)
    metric_keys = list(all_metrics.keys())
    n_metrics = len(metric_keys)

    # Determine grid dimensions for the individual metrics.
    ncols = 3 if n_metrics > 0 else 1
    nrows = int(np.ceil(n_metrics / ncols))

    # Create a figure with GridSpec: if overall_score exists, add an extra row spanning all columns.
    assert overall_score is not None
    fig = plt.figure(figsize=(3 * ncols, 3 * (nrows + 1)))
    gs = gridspec.GridSpec(nrows + 1, ncols, height_ratios=[1] * nrows + [0.6])
    cmap = plt.get_cmap("RdYlGn")
    # Plot individual metrics.
    for i, key in enumerate(metric_keys):
        ax = fig.add_subplot(gs[i])
        val = all_metrics[key]
        color = cmap(val)  # mapping normalized value directly to the colormap
        ax.set_facecolor(color)
        ax.text(0.5, 0.5, f"{val:.2f}", fontsize=16, ha="center", va="center", weight="bold")
        ax.text(0.5, 0.1, key, fontsize=12, ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    # Plot overall score in the bottom row spanning all columns.
    ax_score = fig.add_subplot(gs[nrows, :])
    cmap = plt.get_cmap("RdYlGn")
    color = cmap(overall_score)
    ax_score.set_facecolor(color)
    ax_score.text(0.5, 0.5, f"Overall: {overall_score:.2f}", fontsize=20, ha="center", va="center", weight="bold")
    ax_score.set_xticks([])
    ax_score.set_yticks([])
    for spine in ax_score.spines.values():
        spine.set_visible(False)
    plt.suptitle(metrics["identifier"] + f" ({metrics['doc_type']})", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.show()

    print("Filename: ", metrics["identifier"])
    for metric in METRICS_LIST:
        print(f"{metric}: {metrics[metric]:.3f}")
    if metrics["identifier"] == "Project Results":
        print(f"Total lines: {metrics['line_count']}")
        print(f"Number of files: {metrics['num_files']}")
    print()


# ---------------------------
# Analysis Functions (extended)
# ---------------------------
def analyze_code(code, identifier="unknown"):
    """
    Analyze code and return a dictionary with computed metrics.
    We also count non-blank lines to use for file weighting.
    """
    code_lines = code.splitlines()
    inline_comments, docstrings = extract_comments(code)
    all_comments = [comment for _, comment in inline_comments] + docstrings

    density = compute_comment_density(code, inline_comments, docstrings)  # [0,1]
    readability = compute_readability_scores(all_comments)  # [0,1]
    completeness = check_completeness(code)  # [0,1]
    redundancy = compute_redundancy(inline_comments, code_lines)  # 1 - avg(similarity), [0,1]
    conciseness = check_conciseness(all_comments)  # [0,1]

    accuracy_scores = []
    for line_no, comment in inline_comments:
        if 1 <= line_no <= len(code_lines):
            code_line = code_lines[line_no - 1]
            accuracy_scores.append(evaluate_accuracy(comment, code_line))
    accuracy = np.mean(accuracy_scores) if accuracy_scores else 0

    # Count non-blank lines for weighting
    line_count = sum(1 for line in code_lines if line.strip())

    metrics = {
        "comment_density": density,
        "readability": readability,
        "completeness": completeness,
        "redundancy": redundancy,
        "conciseness": conciseness,
        "accuracy": accuracy
    }

    # Compute a composite file score
    score = compute_file_score(metrics)
    metrics["overall_score"] = score
    metrics["line_count"] = line_count
    metrics["identifier"] = identifier
    return metrics


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    return analyze_code(code, identifier=trim_file_path(file_path))

def trim_file_path(file_path):
    normalized_path = file_path.replace("\\", "/")

    # Search for 'data/' and return from there
    match = re.search(r'data/.*', normalized_path)
    return match.group(0) if match else file_path  # Return trimmed path if found, else return original


def load_dataset(directory):
    """
    Walk through the specified directory, analyze each .py file, and return a DataFrame of metrics.
    Files are labeled as 'LLM' if their filename contains 'llm'; otherwise, 'Human'.
    """
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                metrics = load_single_file(file_path)
                if metrics is not None:
                    results.append(metrics)
    return results


def load_single_file(file_path):
    """
    Load a single file and analyze it.
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        raise FileNotFoundError
    metrics = analyze_file(file_path)
    if metrics is not None:
        label = "LLM" if "llm" in file_path.lower() else "Human"
        metrics["doc_type"] = label
    return metrics


# ---------------------------
# Testing and Main Routine
# ---------------------------
def analyze_single_file(file_name):
    print("Analyzing code snippet...\n")
    metrics = load_single_file(get_file_or_dir_path(file_name))
    # Display the grid for individual metrics
    display_metric_grid(metrics)
    return metrics


def analyze_directory(directory):
    print("Analyzing directory...\n")
    file_results = load_dataset(directory)
    display_project_results(file_results)


def display_project_results(file_results):
    for res in file_results:
        display_metric_grid(res)
    project_metrics = aggregate_project_score(file_results)
    display_metric_grid(project_metrics)


def testme(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            print(file)


def get_file_or_dir_path(file_name=None):
    if file_name is None:
        return os.path.join(os.path.dirname(__file__), '..', 'data')
    return os.path.join(os.path.dirname(__file__), '..', 'data', file_name)


def main():
    dataset_directory = get_file_or_dir_path()
    analyze_directory(dataset_directory)

    # analyze_single_file("sample_code.py")
    # analyze_single_file("sample_code_bad.py")


if __name__ == "__main__":
    main()
