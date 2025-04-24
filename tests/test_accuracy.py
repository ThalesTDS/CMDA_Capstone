from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define test cases: (comment, code)
test_cases = [
    # High-quality matches
    ("Returns the square of a number", "def square(x): return x * x"),
    ("Checks if the input is even", "def is_even(n): return n % 2 == 0"),
    
    # Low-quality matches
    ("This function has nothing to do with squaring", "def square(x): return x * x"),
    ("Does something with strings", "def is_even(n): return n % 2 == 0"),
    
    # Mid Match
    ("Calculates and returns a result", "def square(x): return x * x"),
    ("Checks a condition and gives True or False", "def is_even(n): return n % 2 == 0"),
    
    # Different code sample
    ("Sorts the input list", "def sort_list(lst): return sorted(lst)"),
    ("Returns the first element of a list", "def sort_list(lst): return sorted(lst)"),
    ("Gets the maximum value in the list", "def sort_list(lst): return sorted(lst)"),

    # Vague
    ("This is a function", "def square(x): return x * x"),
    ("Does a task", "def is_even(n): return n % 2 == 0")
]

# Run the test
print("Code-Comment Semantic Similarity Scores:\n")

for i, (comment, code_snippet) in enumerate(test_cases):
    comment_embedding = model.encode(comment, convert_to_tensor=True)
    code_embedding = model.encode(code_snippet, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(comment_embedding, code_embedding).item()

    print(f"Test Case {i+1}:")
    print(f"Comment: {comment}")
    print(f"Code:    {code_snippet}")
    print(f"Similarity Score: {similarity:.4f}\n")