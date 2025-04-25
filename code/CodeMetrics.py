import ast
import warnings
from typing import List, Tuple

import docstring_parser
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sentence_transformers import util
import unixcoder
import torch
nltk.download('punkt_tab', quiet=True)
from globals import model, DOC_TAG_PATTERN, debug


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
        Compute the completeness score for a single function and its docstring.
        """
        if not docstring:
            if debug: print("Method has no docstring")
            return 0.0
        try:
            parsed = docstring_parser.parse(docstring)

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
    def get_function_doc_pairs(code: str) -> List[Tuple[ast.FunctionDef, str]]:
        """
        Extract (function_node, docstring) pairs from source code.
        """
        pairs = []
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    doc = ast.get_docstring(node)
                    pairs.append((node, doc))
        except Exception as e:
            print("AST parsing error in get_function_doc_pairs:", e)
        return pairs

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
        function_doc_pairs = CodeMetrics.get_function_doc_pairs(code)
        if not function_doc_pairs:
            raise RuntimeError(f"Function docstring pairs not found in code: {code}")


        scores = []
        for func_node, docstring in function_doc_pairs:
            score = CodeMetrics.assess_function_completeness(func_node, docstring)
            scores.append(score)

        return sum(scores) / len(scores)

    @staticmethod
    def extract_description_text(docstring: str) -> str:
        """
        Extracts the free-text part of the docstring before any doc section tags.
        """
        match = DOC_TAG_PATTERN.search(docstring)
        if match:
            return docstring[:match.start()].strip()
        return docstring.strip()

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

        if not docstrings or len(docstrings) == 0:
            # TODO: raise RuntimeError(f"Docstrings not found in code: {docstrings}") if preinput parsing
            return 0.0

        # Stop considering docstrings once tags are found (description ended)
        parsed_docstring_descriptions = [
            CodeMetrics.extract_description_text(doc).strip()
            for doc in docstrings
        ]
        # Remove empty descriptions
        filtered_descriptions = [desc for desc in parsed_docstring_descriptions if desc.strip()]
        if not filtered_descriptions:
            # TODO: raise RuntimeError(f"Docstrings all empty in code: {docstrings}") if preinput parsing
            return 0.0

        # Count verbose comments
        verbose_count = 0
        for desc in filtered_descriptions:
            sentences = sent_tokenize(desc)
            for s in sentences:
                if len(s.split()) > verbose_threshold:
                    verbose_count += 1

        embeddings = model.encode(filtered_descriptions)
        similarities = model.similarity(embeddings, embeddings).numpy()
        # since similarity() returns a tensor object, we want a 2D array for simplicity

        row = 0
        similar_count = 0
        for col in range(1, len(filtered_descriptions)):
            if similarities[row, col] >= similarity_threshold:
                similar_count += 1
            else:
                row = col  # move to the next anchor sentence's row index

        # Score computation
        penalty = 0.75 * verbose_count + 0.25 * similar_count
        max_penalty = len(filtered_descriptions) - 0.25
        #            = 0.75 * len(docstrings) + 0.25 * (len(docstrings) - 1)

        return 1 - (penalty / max_penalty)

    @staticmethod
    def evaluate_accuracy(comment: str, code_snippet: str) -> float:
        """
        Evaluate the relevance of a comment by comparing its semantic similarity to the corresponding code snippet.
        Uses a pre-trained BERT-based model (Sentence-BERT) to compute similarity scores.

        :param comment: The comment text.
        :param code_snippet: The corresponding code line.
        :return: The cosine similarity score (between 0 and 1).
        """
        if not comment or not code_snippet:
            raise RuntimeError(f"Comment or code snippet not found: Code: {code_snippet}, Comment: {comment}")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        code_model = unixcoder.UniXcoder("microsoft/unixcoder-base")
        code_model.to(device)
        tokens_ids = code_model.tokenize([code_snippet],max_length=512,mode="<encoder-only>")
        source_ids = torch.tensor(tokens_ids).to(device)
        
        tokens_embeddings, code_embedding = code_model(source_ids)
        
        tokens_ids = code_model.tokenize([comment],max_length=512,mode="<encoder-only>")
        source_ids = torch.tensor(tokens_ids)
        tokens_embeddings,  comment_embedding = code_model(source_ids)
        norm_max_func_embedding = torch.nn.functional.normalize(code_embedding, p=2, dim=1)
        norm_comment_embedding = torch.nn.functional.normalize(comment_embedding, p=2, dim=1)
        similarity = torch.einsum("ac,bc->ab",norm_max_func_embedding, norm_comment_embedding)
      
        return similarity.item()
        


    @staticmethod
    def extract_comment_code_pairs(source: str) -> List[Tuple[str, str]]:
        lines = source.splitlines()
        pairs = []
        n = len(lines)

        # Get docstring lines using AST
        try:
            tree = ast.parse(source)
            docstring_lines = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                    doc = ast.get_docstring(node)
                    if doc and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                        first_line = node.body[0].lineno - 1
                        docstring_lines.update(range(first_line, first_line + doc.count('\n') + 1))
        except SyntaxError:
            docstring_lines = set()

        def is_hanging_string(line: str) -> bool:
            stripped = line.strip()
            return (
                    (stripped.startswith('"') or stripped.startswith("'")) and
                    (stripped.endswith('"') or stripped.endswith("'")) and
                    not (stripped.startswith('"""') or stripped.startswith("'''")) and
                    len(stripped) > 1
            )

        def is_code_line(line: str) -> bool:
            return bool(line.strip()) and not line.strip().startswith("#") and not is_hanging_string(line)

        i = 0
        while i < n - 1:
            line = lines[i].strip()
            next_line = lines[i + 1].strip()

            if i in docstring_lines or (i + 1) in docstring_lines:
                i += 1
                continue

            # # comment followed by real code
            if line.startswith("#") and is_code_line(next_line):
                pairs.append((line, next_line))
                i += 2
                continue

            # hanging string comment followed by real code
            if is_hanging_string(line) and is_code_line(next_line):
                pairs.append((line, next_line))
                i += 2
                continue

            i += 1

        return pairs

    @staticmethod
    def compute_accuracy_scores(code: str, inline_comments: List[str]) -> float:
        accuracy_scores = []
        # Extract code-comment pairs
        code_comment_pairs = CodeMetrics.extract_comment_code_pairs(code)
        # Iterate through the pairs and compute accuracy scores
        for comment_part, code_part  in code_comment_pairs:
            # Remove leading/trailing whitespace
            code_part = code_part.strip()
            comment_part = comment_part.strip()

            # Skip empty lines
            if not code_part or not comment_part or len(code_part) < 3 or len(comment_part) < 3:
                continue

            # Compute accuracy score
            accuracy_scores.append(CodeMetrics.evaluate_accuracy(code_part, comment_part))
            if debug:
                print(f"Code Part: {code_part} Comment Part: {comment_part}  Accuracy Score: {accuracy_scores[-1]}")

        for line in inline_comments:
            code_part, comment_part = line.split('#', 1)
            accuracy_scores.append(CodeMetrics.evaluate_accuracy(code_part, comment_part))
            if debug:
                print(f"Code Line: {code_part} Comment: {comment_part}  Accuracy Score: {accuracy_scores[-1]}")
        return np.mean(accuracy_scores) if accuracy_scores else 0.0
