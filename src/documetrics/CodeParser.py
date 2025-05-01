import ast
import warnings
from typing import List, Tuple

from documetrics.globals import DOC_TAG_PATTERN


# =============================================================================
# Code Parsing & Extraction
# =============================================================================
class CodeParser:
    @staticmethod
    def extract_comments(code: str, inline: bool = False) -> List[str] | Tuple[List[str], List[str]]:
        """
        Extract docstrings and optionally inline comments (deprecated) from the provided source code.

        :param code: The source code as a string.
        :param inline: If True, include inline comments in the output.
        :return: List of docstrings or a tuple of (docstrings, inline comments).
        """
        docstrings = []
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    doc = ast.get_docstring(node)
                    if doc:
                        docstrings.append(doc)
        except Exception as e:
            print("Error in CodeParser.extractcomments -- AST error:", e)
        if inline:
            inline_comment_lines = []
            for line in code.splitlines():
                # strip the line to remove leading and trailing whitespace
                line = line.strip()
                if '#' in line:
                    before, after = line.split('#', 1)
                    # 3 characters minimum for code (x=1), 4 for comment (could be more)
                    if len(before.strip()) >= 3 and len(after.strip()) >= 4:
                        inline_comment_lines.append(line)
            return docstrings, inline_comment_lines

        return docstrings

    @staticmethod
    def get_function_doc_pairs(code: str) -> List[Tuple[ast.FunctionDef, str]]:
        """
        Extracts all function definitions and their associated docstrings from the given source code.

        :param code: The source code as a string.
        :return: A list of tuples, where each tuple contains a function definition node and its docstring.
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
    def extract_description_text(docstring: str) -> str:
        """
        Extract the free-text part of a docstring before any section tags.

        This function identifies and removes structured tags (e.g., parameter or return
        sections) from a docstring, leaving only the descriptive text.

        :param docstring: The full docstring to process.
        :return: The descriptive text portion of the docstring.
        """
        match = DOC_TAG_PATTERN.search(docstring)
        if match:
            return docstring[:match.start()].strip()
        return docstring.strip()
