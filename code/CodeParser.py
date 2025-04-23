import ast
import io
import tokenize
from typing import List, Tuple, Optional


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
