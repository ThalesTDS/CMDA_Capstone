import re
from sentence_transformers import SentenceTransformer, util

class AccuracyEvaluator:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    @staticmethod
    def evaluate_accuracy_overlap(comment: str, code_snippet: str) -> float:
        """
        Evaluate the relevance of a comment by comparing overlapping identifier tokens with the code snippet.
        
        :param comment: The comment text.
        :param code_snippet: The corresponding code line.
        :return: The ratio of overlapping tokens (between 0 and 1).
        """
        code_tokens = set(re.findall(r'\b\w+\b', code_snippet))
        comment_tokens = set(re.findall(r'\b\w+\b', comment))
        if not code_tokens:
            return 0.0
        overlap = code_tokens.intersection(comment_tokens)
        return len(overlap) / len(code_tokens)
    
    @staticmethod
    def evaluate_accuracy_bert(comment: str, code_snippet: str) -> float:
        """
        Evaluate the relevance of a comment by comparing its semantic similarity to the corresponding code snippet.
        Uses a pre-trained BERT-based model (Sentence-BERT) to compute similarity scores.
        
        :param comment: The comment text.
        :param code_snippet: The corresponding code line.
        :return: The cosine similarity score (between 0 and 1).
        """
        comment_embedding = AccuracyEvaluator.model.encode(comment, convert_to_tensor=True)
        code_embedding = AccuracyEvaluator.model.encode(code_snippet, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(comment_embedding, code_embedding)
        return similarity.item()
    
# Mini test for context understanding
def test_accuracy_methods():
    test_cases = [
        ("Check if x is positive", "if x > 0:"),
        ("Verify that x is greater than zero", "if x > 0:"),
        ("Ensure x is non-negative", "if x >= 0:"),
        ("Loop through all elements in the list", "for item in my_list:"),
        ("Iterate over the array", "for item in my_list:"),
    ]
    
    print("\nTesting Accuracy Methods:\n")
    for comment, code in test_cases:
        overlap_score = AccuracyEvaluator.evaluate_accuracy_overlap(comment, code)
        bert_score = AccuracyEvaluator.evaluate_accuracy_bert(comment, code)
        print(f"Comment: '{comment}'\nCode: '{code}'")
        print(f"Overlap Score: {overlap_score:.4f}")
        print(f"BERT Score: {bert_score:.4f}")
        print("-" * 50)
    
if __name__ == "__main__":
    test_accuracy_methods()
