import unittest
from DocuMetrics import CodeMetrics

class TestCodeMetrics(unittest.TestCase):
    def setUp(self):
        """Sample code snippets for testing."""
    
        self.code_with_comments = """
        # This is a test function
        def add(a, b):
            \"\"\"
            Adds two numbers together.

            @param a: First number
            @param b: Second number
            @return: Sum of a and b
            \"\"\"
            return a + b
            """

        self.code_without_comments = """
        def multiply(a, b):
            return a * b
            """

        self.inline_comments = [(1, "# This is a test function")]

        self.docstrings = ["""
        Adds two numbers together.

        @param a: First number
        @param b: Second number
        @return: Sum of a and b
        """] 


    def test_compute_comment_density(self):
        density = CodeMetrics.compute_comment_density(self.code_with_comments, self.inline_comments, self.docstrings)
        self.assertGreater(density, 0, "Comment density should be greater than 0")
    
    def test_compute_readability_scores(self):
        readability = CodeMetrics.compute_readability_scores(["This is a simple comment.", "Complexity of syntax is significant."])
        self.assertGreaterEqual(readability, 0, "Readability score should be non-negative")
        self.assertLessEqual(readability, 1, "Readability score should be at most 1")

    def test_check_completeness(self):
        completeness = CodeMetrics.check_completeness(self.code_with_comments, self.docstrings[0])
        self.assertGreater(completeness, 0, "Completeness score should be greater than 0 if docstring exists")
            
    def test_compute_redundancy(self):
        redundancy = CodeMetrics.compute_redundancy(["# Loop through the list", "# Iterate over elements in the list"], [])
        self.assertGreaterEqual(redundancy, 0, "Redundancy score should be non-negative")
        self.assertLessEqual(redundancy, 1, "Redundancy score should be at most 1")
    
    def test_check_conciseness(self):
        conciseness = CodeMetrics.check_conciseness(["This is a concise comment.", "This comment is extremely long and verbose, explaining things in an unnecessary manner way beyond what is required."])
        self.assertGreaterEqual(conciseness, 0, "Conciseness score should be non-negative")
        self.assertLessEqual(conciseness, 1, "Conciseness score should be at most 1")

if __name__ == "__main__":
    unittest.main()
