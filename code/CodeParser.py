import ast
import warnings
from typing import List, Tuple


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
