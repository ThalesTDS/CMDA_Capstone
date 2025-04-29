import ast
import warnings

from typing import List, Tuple



# =============================================================================
# Code Parsing & Extraction
# =============================================================================
class CodeParser:
    @staticmethod
    def extract_comments(code: str) -> Tuple[List[str], List[str], List[int]]:
        """
        Extract inline comments and docstrings from the provided source code.

        :param code: The source code as a string.
        :return: A tuple where the first element is a list of inline comments, the second
                 element is a list of docstring texts, and the third element is a list of comment
                 and docstring counts.
        """
        count_comments = 0
        inline_comment_lines = []
        for line in code.splitlines():
            # strip the line to remove leading and trailing whitespace
            line = line.strip()
            if '#' in line:
                before, after = line.split('#', 1)
                # 3 characters minimum for code (x=1), 4 for comment (could be more)
                if len(before.strip()) >= 3 and len(after.strip()) >= 4:
                    inline_comment_lines.append(line)
                    count_comments += 1

        count_docstrings = 0
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
                        count_docstrings += 1
        except Exception as e:
            print("Error in CodeParser.extractcomments -- AST error:", e)
        counts = [count_comments, count_docstrings]

        return inline_comment_lines, docstrings, counts
