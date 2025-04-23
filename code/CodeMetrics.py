import ast
from typing import List, Tuple

import numpy as np
from sentence_transformers import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from globals import model


# =============================================================================
# Metrics Calculation
# =============================================================================
class CodeMetrics:

    @staticmethod
    def compute_comment_density(code: str,
                                inline_comments: List[Tuple[int, str]],
                                docstrings: List[str]) -> float:
        """
        Compute the normalized comment density of the source code.

        :param code: The source code as a string.
        :param inline_comments: List of tuples (line number, inline comment).
        :param docstrings: List of docstring texts.
        :return: Normalized comment density score between 0 and 1.
        """
        lines = code.splitlines()
        total_lines = sum(1 for line in lines if line.strip() != "")

        # Unique inline comment lines.
        comment_line_numbers = {line_no for line_no, _ in inline_comments}
        inline_comment_lines = len(comment_line_numbers)

        # Count docstring lines.
        docstring_lines = sum(len(doc.splitlines()) for doc in docstrings)
        total_comment_lines = inline_comment_lines + docstring_lines
        density = total_comment_lines / total_lines if total_lines > 0 else 0

        return CodeMetrics.normalize_comment_density(density)

    @staticmethod
    def normalize_comment_density(ratio: float,
                                  ideal_low: float = 0.1,
                                  ideal_high: float = 0.3,
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
    def compute_completeness(code: str, docstring: str) -> float:
        """
        Check if the docstring contains required elements based on function/class definition.

        :param code: The full source code containing the function/class.
        :param docstring: The function/class docstring.
        :return: A completeness score between 0 (incomplete) and 1 (fully complete).
        """
        if not docstring:
            return 0.0

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):  # Check function definitions
                    param_names = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]
                    has_return = isinstance(node.returns, ast.Name)  # Checks if a return type is declared

                    needs_param = len(param_names) > 0  # Function requires @param if it has parameters
                    needs_return = has_return  # Function requires @return if return type exists

                    # Check if the docstring contains necessary components
                    has_param_doc = all(
                        f"@param {param}" in docstring for param in param_names) if needs_param else True
                    has_return_doc = "@return" in docstring if needs_return else True
                    has_general_desc = len(
                        docstring.strip().split("\n")[0].split()) > 5  # At least 5 words in first line

                    # Calculate completeness score
                    completeness_score = 0.0
                    if has_general_desc:
                        completeness_score += 0.5  # General description contributes 50%
                    if needs_param and has_param_doc:
                        completeness_score += 0.25  # Parameter documentation is 25%
                    if needs_return and has_return_doc:
                        completeness_score += 0.25  # Return documentation is 25%

                        # Check if the docstring contains a general description (not just `@param` and `@return`)
                        docstring_lines = docstring.strip().split("\n")
                        first_line = docstring_lines[0].strip() if docstring_lines else ""
                        has_general_description = len(first_line.split()) > 5  # Requires at least 5 words

                        # Calculate completeness score
                        completeness_score = 0.0
                        if has_general_description:
                            completeness_score += 0.4  # General description carries 40% weight
                        if needs_param and "@param" in docstring:
                            completeness_score += 0.3  # Params contribute 30% to completeness
                        if needs_return and "@return" in docstring:
                            completeness_score += 0.3  # Return doc contributes 30%

                        return completeness_score
        except SyntaxError:
            return 0.0  # Fallback in case of syntax issues

        return 1.0  # Default case (should never reach here)

    @staticmethod
    def compute_similarity(text1: str, text2: str) -> float:
        """
        Compute the cosine similarity between two texts using TF-IDF.

        :param text1: The first text string.
        :param text2: The second text string.
        :return: Cosine similarity score between 0 and 1. Returns 0 if either text is empty.
        """
        if not text1.strip() or not text2.strip():
            return 0.0
        try:
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([text1, text2])
            sim_matrix = cosine_similarity(vectors)
            return sim_matrix[0, 1]
        except ValueError:
            return 0.0

    @staticmethod
    def compute_conciseness(comments: List[str], verbose_threshold: int = 20,
                            similarity_threshold: float = .70) -> float:
        """
        Detect how concise comments are using similarity and wordy sentences. Sentences are considered wordy if they
        pass a designated threshold and the same follows for similarity. By default, verbose threshold is 20 words in a sentence,
        and similarity is .50. If the score is high, then conciseness is worse and vice versa. Therefore, we compute the conciseness by
        dividing our weighted score with a maximum score. We subtract it from 1. This way, we have a score between 0 and 1, with a lower score
        being a worse level of conciseness

        :param comments: List of comment strings.
        :param verbose_threshold: Word count threshold to consider a comment as verbose.
        :return: Score between 0 and 1 where 1 means all comments are concise.
        """
        embeddings = model.encode(comments)
        similarities = model.similarity(embeddings,
                                        embeddings).numpy()  # since similarity() returns a tensor object, we want a 2D array for simplicity

        """
            This algorithm is a bit tricky to understand, but I will walk you through. Our similarity scores is a tensor matrix. To simplify
            its usage, I turned it into a numpy array that 2-D. Since we have n sentences, our matrix is n by n. To check if each sentence
            passes our similarity and verbose threshold, I iterate through a row, with our anchor sentence being the col at the same index
            as row. So, if are are row 0, then we start from col 0. If we are at row 3, we iterate through the row starting at col 3. Initially
            we set our anchor before the loop to make things easier. If each similarity score is above our threshold, we have only gone
            through the first row and are done. If a sentence is below the threshold, we use that sentence as the new anchor point by moving
            to its corresponding index within the column. Then, we start from that index and continue iterating through the columns

        """
        ncols = len(similarities)  # our 2D array is a square matrix, so we only need length of one dimension
        row = 0

        verbose_count = 0
        if len(comments[0]) > verbose_threshold:
            verbose_count = 1

        similar_count = 0
        for col in range(1, ncols):

            if similarities[row, col] >= similarity_threshold:
                similar_count += 1

            else:
                row = col  # move to the next anchor sentence's row index
            if len(comments[col]) > verbose_threshold:
                verbose_count += 1

        score = .75 * verbose_count + .25 * similar_count

        dim = len(comments) * len(comments)

        return 1 - (score / dim)

    @staticmethod
    def evaluate_accuracy(comment: str, code_snippet: str) -> float:
        """
        Evaluate the relevance of a comment by comparing its semantic similarity to the corresponding code snippet.
        Uses a pre-trained BERT-based model (Sentence-BERT) to compute similarity scores.

        :param comment: The comment text.
        :param code_snippet: The corresponding code line.
        :return: The cosine similarity score (between 0 and 1).
        """
        comment_embedding = model.encode(comment, convert_to_tensor=True)
        code_embedding = model.encode(code_snippet, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(comment_embedding, code_embedding)
        return similarity.item()

    @staticmethod
    def compute_accuracy_scores(inline_comments: List[Tuple[int, str]], code_lines: List[str]) -> float:
        accuracy_scores = []
        for line_no, comment in inline_comments:
            if 1 <= line_no <= len(code_lines):
                code_line = code_lines[line_no - 1]
                accuracy_scores.append(CodeMetrics.evaluate_accuracy(comment, code_line))
        return np.mean(accuracy_scores) if accuracy_scores else 0.0
