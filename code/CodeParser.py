import ast
from typing import List, Tuple, Optional


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
            hash_index = line.find('#')
            if hash_index > 0:
                before = line[:hash_index]
                if sum(c.strip() != '' for c in before) >= 3:
                    inline_comment_lines.append(line.rstrip())
                    count_comments += 1

        count_docstrings = 0
        docstrings = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                    doc = ast.get_docstring(node)
                    if doc:
                        docstrings.append(doc)
                        count_docstrings += 1
        except Exception as e:
            print("AST error:", e)
        counts = [count_comments, count_docstrings]

        return inline_comment_lines, docstrings, counts

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
