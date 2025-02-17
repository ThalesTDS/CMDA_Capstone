# Code Analysis Tool

## Overview
This tool is designed to analyze Python source code files and compute various metrics related to code quality, readability, and documentation. The analysis results can be aggregated at both the file and project levels, providing insights into how well-documented and readable a given codebase is.

## Features
- Extracts and evaluates inline comments and docstrings.
- Computes multiple metrics including comment density, readability, completeness, redundancy, conciseness, and accuracy.
- Normalizes metric values for meaningful comparisons.
- Aggregates scores across multiple files for a holistic project assessment.
- Provides visual representations of metric scores.

## Components

### **1. Code Parsing & Extraction**
#### `CodeParser`
- **`extract_comments(code: str) -> Tuple[List[Tuple[int, str]], List[str]]`**
  - Extracts inline comments and docstrings from the given source code.
- **`get_ast(code: str) -> Optional[ast.AST]`**
  - Parses the code into an Abstract Syntax Tree (AST) for further analysis.

### **2. Metrics Calculation**
#### `CodeMetrics`
- **`compute_comment_density(code, inline_comments, docstrings) -> float`**
  - Computes the proportion of comment lines to total lines.
- **`normalize_comment_density(ratio) -> float`**
  - Normalizes the comment density to a meaningful score.
- **`compute_readability_scores(comments) -> float`**
  - Calculates readability using the Flesch Reading Ease score.
- **`check_completeness(code) -> float`**
  - Evaluates whether functions and classes have sufficient docstring coverage.
- **`compute_similarity(text1, text2) -> float`**
  - Uses TF-IDF and cosine similarity to measure textual similarity.
- **`compute_redundancy(inline_comments, code_lines) -> float`**
  - Analyzes redundancy by comparing comments to corresponding code lines.
- **`check_conciseness(comments, verbose_threshold) -> float`**
  - Measures conciseness by checking for excessively verbose comments.
- **`evaluate_accuracy(comment, code_snippet) -> float`**
  - Compares comment relevance by checking for overlapping tokens with the code.

### **3. Aggregate Scoring**
#### `ScoreAggregator`
- **`compute_file_score(metrics) -> float`**
  - Computes an overall weighted score for a single file.
- **`aggregate_project_score(file_results) -> Dict[str, Any]`**
  - Aggregates scores across multiple files, weighted by line count.

### **4. Display Functions**
#### `MetricsDisplay`
- **`display_metric_grid(metrics) -> None`**
  - Generates a visual representation of metrics in a grid format.

### **5. File and Project Analysis**
#### `CodeAnalyzer`
- **`analyze_code(code, identifier) -> Dict[str, Any]`**
  - Computes all metrics for a given code snippet.
- **`analyze_file(file_path) -> Optional[Dict[str, Any]]`**
  - Reads and analyzes a Python file.

#### `FileLoader`
- **`load_single_file(file_path) -> Optional[Dict[str, Any]]`**
  - Loads and analyzes a single Python file.
- **`load_dataset(directory) -> List[Dict[str, Any]]`**
  - Walks through a directory and analyzes all `.py` files.

#### `ProjectAnalyzer`
- **`display_project_results(file_results) -> None`**
  - Displays individual file metrics and aggregated project results.
- **`analyze_directory(directory) -> None`**
  - Runs analysis on all Python files in a directory.

### **6. Main Routine**
#### `main()`
- Entry point for running the tool.
- Analyzes all Python files in the specified dataset directory.

## How It Works
1. The tool extracts comments and docstrings from Python files.
2. Various metrics are computed for each file, evaluating documentation quality and readability.
3. Metrics are normalized and aggregated to provide overall scores.
4. Results are displayed using a grid visualization.
5. Users can analyze a single file or an entire directory of Python files.