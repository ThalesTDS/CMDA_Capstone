import ast
import re
import warnings
from functools import lru_cache
from typing import List, Tuple

import docstring_parser
import nltk
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab', quiet=True)

from src import unixcoder
from src.CodeParser import CodeParser

from src.globals import debug

# Set the device to GPU if available, otherwise fallback to CPU
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the UniXcoder model and move it to the selected device
_unixcoder = unixcoder.UniXcoder("microsoft/unixcoder-base").to(_device).eval()

# Initialize the MiniLM-L6-v2 model for semantic comparison within conciseness metric
_miniLM = SentenceTransformer("all-MiniLM-L6-v2", device=str(_device))


def _embed(text: str) -> torch.Tensor:
    """
    Generate an L2-normalized embedding for the given text using the UniXcoder model.

    This function tokenizes the input text, processes it through the UniXcoder model,
    and normalizes the resulting embedding vector using L2 normalization.

    :param text: The input text to embed.
    :return: A PyTorch tensor containing the L2-normalized embedding.
    """
    token_ids = _unixcoder.tokenize([text], max_length=512, mode="<encoder-only>")
    src = torch.tensor(token_ids).to(_device)
    _, emb = _unixcoder(src)
    return torch.nn.functional.normalize(emb, p=2, dim=1)


@lru_cache(maxsize=512)
def _parse_docstring(ds: str):
    """
    Parse a docstring and cache the result.

    This function wraps the `docstring_parser.parse()` method with an LRU cache
    to improve performance when parsing the same docstring multiple times.

    :param ds: The docstring to parse.
    :return: A parsed representation of the docstring.
    """
    return docstring_parser.parse(ds)


# =============================================================================
# Metrics Calculation
# =============================================================================
class CodeMetrics:

    @staticmethod
    def compute_comment_density(code_lines: List[str]) -> float:
        """
        Compute the normalized comment density of the source code.

        :param code_lines: The source code as a string.
        :return: Normalized comment density score between 0 and 1.
        """
        count_comment_lines = 0
        count_code_lines = 0
        in_multiline_string = False

        for line in code_lines:
            stripped = line.strip()
            if not stripped or len(stripped) < 3:
                continue

            # Detect triple-quoted strings used as comments (docstrings or blocks)
            if stripped.startswith(("'''", '"""')):
                if in_multiline_string:
                    count_comment_lines += 1
                    in_multiline_string = False
                else:
                    count_comment_lines += 1
                    if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                        in_multiline_string = True
                continue
            elif in_multiline_string:
                count_comment_lines += 1
                continue

            if stripped.startswith('#'):
                count_comment_lines += 1
            elif '#' in stripped:
                count_comment_lines += 1
                count_code_lines += 1
            else:
                count_code_lines += 1

        total_relevant_lines = count_code_lines + count_comment_lines
        if total_relevant_lines == 0:
            raise ValueError("No comment or code lines found in the code. call: CodeMetrics.compute_comment_density")
        density = (count_comment_lines / total_relevant_lines)
        if debug:
            print(f"Comment Density: {density:.2f} ({count_comment_lines}/{total_relevant_lines})")

        return CodeMetrics.normalize_comment_density(density)

    @staticmethod
    def normalize_comment_density(ratio: float,
                                  ideal_low: float = 0.1,
                                  ideal_high: float = 0.35,
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
    def assess_function_completeness(func_node: ast.FunctionDef, docstring: str | None) -> float:
        """
        Assess the completeness of a function's docstring.

        This function evaluates the provided docstring against the function definition
        to determine if it includes a general description, parameter documentation,
        and return type information. The completeness score is calculated based on
        these elements.

        :param func_node: The AST node representing the function definition.
        :param docstring: The docstring associated with the function, or None if absent.
        :return: A float score between 0.0 (incomplete) and 1.0 (fully complete).
        """
        if not docstring:
            if debug: print("Method has no docstring")
            return 0.0
        try:
            parsed = _parse_docstring(docstring)

            # General description (minimum 2 words)
            has_desc = parsed.short_description is not None and len(parsed.short_description.split()) >= 2

            # Parameters
            param_names = [arg.arg for arg in func_node.args.args if arg.arg not in ("self", "cls")]
            doc_param_names = {p.arg_name for p in parsed.params}
            has_all_params = all(name in doc_param_names for name in param_names)

            # Return
            has_return_annot = func_node.returns is not None
            has_return_doc = parsed.returns is not None if has_return_annot else True

            # Weights: 40% desc, 30% params, 30% return
            score = 0.0
            if has_desc:
                if debug: print("has_desc")
                score += 0.4
            if param_names and has_all_params:
                if debug: print("has_all_params")
                score += 0.3
            if has_return_annot and has_return_doc:
                if debug: print("has_return_annot and has_return_doc")
                score += 0.3
            elif not has_return_annot:
                if debug: print("no return found")
                score += 0.3  # Return not expected, grant credit

            return score

        except Exception as e:
            print("Docstring parsing error in assess_function_completeness:", e)
            return 0.0

    @staticmethod
    def compute_completeness(code: str) -> float:
        """
        Check if the docstring contains required elements based on function/class definition.
        Supports the following Docstring Formats:
            ReStructured Text (reST), Google, NumPy/SciPy, EpYtext
        DOES NOT support the combination of the above.

        :param code: The full source code containing the function/class.
        :return: A completeness score between 0 (incomplete) and 1 (fully complete).
        """
        function_doc_pairs = CodeParser.get_function_doc_pairs(code)
        if not function_doc_pairs:
            print(f"Function docstring pairs not found in code: {code}")
            return 0.0

        scores = []
        for func_node, docstring in function_doc_pairs:
            score = CodeMetrics.assess_function_completeness(func_node, docstring)
            scores.append(score)

        return np.round(sum(scores) / len(scores), 4)

    @staticmethod
    def compute_conciseness(docstrings: List[str], verbose_threshold: int = 20,
                            similarity_threshold: float = .70) -> float:
        """
       Compute the conciseness score of a list of docstrings.

       A sentence is considered verbose if it exceeds `verbose_threshold` words.
       A sentence is considered redundant if it is too similar to a preceding comment
       (based on cosine similarity ≥ `similarity_threshold`). Only sequential comparisons are made.

       The final score penalizes verbosity (75%) and local redundancy (25%), and normalizes
       the penalty to return a score between 0 and 1, where 1 means ideally concise.

       :param docstrings: List of docstrings.
       :param verbose_threshold: Maximum acceptable word count for a single comment.
       :param similarity_threshold: Cosine similarity threshold for considering two comments redundant.
       :return: A score between 0 (not concise) and 1 (ideally concise).
       """

        if not docstrings:
            raise RuntimeError("Docstrings not found in code -- CodeMetrics.compute_conciseness")

        # Stop considering docstrings once tags are found (description ended)
        parsed_docstring_descriptions = [
            CodeParser.extract_description_text(doc).strip()
            for doc in docstrings
        ]
        # Remove empty descriptions
        filtered_descriptions = [desc for desc in parsed_docstring_descriptions if desc.strip()]
        if not filtered_descriptions:
            return 0.0
        count_sentences = 0
        # Count verbose comments
        verbose_count = 0
        for desc in filtered_descriptions:
            sentences = sent_tokenize(desc)
            for s in sentences:
                count_sentences += 1
                if len(s.split()) > verbose_threshold:
                    verbose_count += 1

        embeddings = _miniLM.encode(filtered_descriptions)
        similarities = _miniLM.similarity(embeddings, embeddings).numpy()
        # since similarity() returns a tensor object, we want a 2D array for simplicity

        row = 0
        similar_count = 0
        for col in range(1, len(filtered_descriptions)):
            count_sentences += 1
            if similarities[row, col] >= similarity_threshold:
                similar_count += 1
            else:
                row = col  # move to the next anchor sentence's row index

        # Score computation
        penalty = 0.75 * verbose_count + 0.25 * similar_count
        max_penalty = max(1e-6, count_sentences - 0.25)
        #            = 0.75 * count_sentences + 0.25 * (count_sentences - 1)

        return max(0, 1 - (penalty / max_penalty))

    @staticmethod
    def get_description_and_code(code: str) -> List[Tuple[str, str]]:
        """
        Extracts (docstring, cleaned function body) pairs from Python source code.
        Cleans out comments while preserving structure.

        :param code: String containing the Python source code.
        :return: List of (docstring, function_body) tuples.
        """
        lines = code.splitlines(keepends=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code)

        functions = []
        all_docstring_lines = set()
        function_bodies = []

        # Preprocess: collect all functions and their ranges
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno - 1
                indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                end_line = start_line + 1
                while end_line < len(lines):
                    line = lines[end_line]
                    if line.strip() == "" or line.lstrip().startswith("#"):
                        end_line += 1
                        continue
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent:
                        break
                    end_line += 1
                function_bodies.append((start_line, end_line, node))

                # Capture docstring line spans
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value,
                                                                                   (ast.Str, ast.Constant)):
                    doc_start = node.body[0].lineno - 1
                    doc_end = node.body[0].end_lineno
                    all_docstring_lines.update(range(doc_start, doc_end))

        # Sort by start_line to ensure nested functions come after parents
        function_bodies.sort()

        # Create a map of nested function spans to skip in outer bodies
        all_function_spans = [(start, end) for start, end, _ in function_bodies]

        for start_line, end_line, node in function_bodies:
            full_docstring = ast.get_docstring(node) or ""
            description = CodeParser.extract_description_text(full_docstring)

            cleaned_lines = []
            for idx in range(start_line, end_line):
                # Skip docstring lines
                if idx in all_docstring_lines:
                    continue

                # Skip lines that belong to nested functions
                if any(start_line < n_start <= idx < n_end for n_start, n_end in all_function_spans):
                    continue

                line = lines[idx]
                stripped = line.lstrip()
                if stripped.startswith("#") or stripped == "":
                    continue
                code_without_comment = re.split(r'\s+#', line, maxsplit=1)[0]
                cleaned_lines.append(code_without_comment.rstrip())

            cleaned_function_body = '\n'.join(cleaned_lines)
            functions.append((description, cleaned_function_body))
        if debug:
            for desc, body in functions:
                print(f"Description: {desc}\n Body: {body}")

        return functions

    @staticmethod
    def compute_accuracy_scores(code: str) -> float:
        """
        Compute the accuracy score between code and its corresponding docstring.

        This function extracts pairs of docstrings and their associated code,
        generates embeddings for both using the `_embed` function, and calculates
        the cosine similarity between the embeddings. The mean similarity score
        is returned as the accuracy score.

        :param code: The Python source code as a string.
        :return: A float representing the mean similarity score between code and docstrings.
        """
        pairs = CodeMetrics.get_description_and_code(code)
        if not pairs:
            return 0.0

        flat = [txt for p in pairs for txt in p]  # [code0, doc0, …]
        embeds = torch.cat([_embed(t) for t in flat])
        sims = torch.einsum("ac,ac->a", embeds[0::2], embeds[1::2])
        return sims.mean().item()
