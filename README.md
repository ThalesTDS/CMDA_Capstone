# DocuMetrics: Code Documentation Quality Analyzer
`pip install .` Within the project folder to install all dependencies.

## Overview
DocuMetrics analyzes Python source code for the presence and quality of inline comments and docstrings. It computes documentation-related metrics and provides a composite score for each file and project.
## Features
- Extracts and evaluates inline comments and docstrings.
- Computes multiple metrics including comment density, readability, completeness, redundancy, conciseness, and accuracy.
- Normalizes metric values for meaningful comparisons.
- Aggregates scores across multiple files for a holistic project assessment.
- Provides visual representations of metric scores.

---

## Components

### **1. Code Parsing & Extraction**
#### `CodeParser`
- **`extract_comments(code: str) -> Tuple[List[str], List[str], List[int]]`**
  - Extracts inline comments (with ≥3 non-whitespace chars before `#` and ≥4 after) and docstrings from source code.
  - Returns inline comment lines, extracted docstrings, and their respective counts.
- **Uses `ast.parse()` with BOM-safe reading and warnings suppressed.**

---

### **2. Metrics Calculation**
#### `CodeMetrics`
- **`compute_comment_density(code_lines: List[str]) -> float`**
  - Measures the density of comment lines (inline or full-line) relative to code lines.
- **`normalize_comment_density(ratio: float) -> float`**
  - Scores density based on an ideal range (0.1 to 0.35) using linear normalization.
- **`compute_completeness(code: str) -> float`**
  - Assesses docstring structure (description, parameter coverage, return info) using `docstring_parser`.
- **`compute_conciseness(docstrings: List[str], verbose_threshold=20, similarity_threshold=0.70) -> float`**
  - Penalizes verbose and redundant docstrings using token count and cosine similarity (Sentence-BERT).
- **`evaluate_accuracy(comment: str, code_snippet: str) -> float`**
  - Compares a comment’s semantic relevance to its associated code using Sentence-BERT.
- **`compute_accuracy_scores(inline_comments: List[str]) -> float`**
  - Aggregates accuracy scores for inline comments.

---

### **3. File-Level Analysis**
#### `CodeAnalyzer`
- **`analyze_code(code: str, identifier: str) -> Optional[Dict[str, Any]]`**
  - Evaluates code using all metrics and returns a dictionary with scores and metadata.
  - Filters out files with fewer than 3 inline comments or 2 docstrings.
- **`analyze_file(file_path: str) -> Optional[Dict[str, Any]]`**
  - Reads a Python file (UTF-8 with BOM support) and analyzes it.

---

### **4. File and Project Management**
#### `FileLoader`
- **`load_single_file(file_path: str) -> Optional[Dict[str, Any]]`**
  - Analyzes a single `.py` file and assigns it a "Human" or "LLM" label.
- **`load_dataset(directory: str) -> List[Dict[str, Any]]`**
  - Recursively analyzes all `.py` files in a directory.
- **`get_dir_path(sub_folder_name: Optional[str]) -> str`**
  - Builds the path to a dataset directory (inside `data/`).

---

### **5. Aggregate Scoring**
#### `ScoreAggregator`
- **`compute_file_score(metrics: Dict[str, float]) -> float`**
  - Combines individual metric scores into a single weighted file score.
- **`aggregate_project_score(file_results: List[Dict[str, Any]]) -> Dict[str, Any]`**
  - Aggregates metrics across multiple files, weighted by line count.
  - Detects project type: Human, LLM, or Mixed.

---

### **6. Metric Visualization**
#### `Dashboard`


---

### **7. Project-Level Execution**
#### `ProjectAnalyzer`
- **`analyze_directory(directory: str) -> None`**
  - Runs analysis on all `.py` files in the given directory.
- **`display_project_results(file_results: List[Dict[str, Any]]) -> None`**
  - Displays per-file and project-level visual summaries.

---

### **8. Main Routine**
#### `main()`
- Loads a dataset directory and runs a full analysis + visualization.

## How It Works
1. The tool extracts comments and docstrings from Python files.
2. Various metrics are computed for each file, evaluating documentation quality.
3. Metrics are normalized and aggregated to provide overall scores.
4. Results are displayed within the dashboard.
5. Users can analyze a single file or an entire directory of Python files.