### **Accuracy**
- Does not rlly work

### **Comment Density**
- Should doc strings and imports count? Currently they do.

### **Completeness**
- Review weighting.

### **Conciseness**
- Review weighting.



### **General**
- Create/Find sample code to run tests on.
- Adjust weighting of metrics.

### **Readability**
- They only measure how "easy" a comment is to read, not if it makes sense.
- Nonsense text like "34653efgdfg" still gets scored based on sentence structure and word length.
- Im debugging it (Amy)

**Pre-trained Language Models (Best Option)**
BERT-based Models (Sentence Transformers)

Models like all-MiniLM-L6-v2 can check if comments contain meaningful sentences.
Can be fine-tuned on high-quality comments to predict validity.
How to Use:

Encode the comment and compare it against well-written reference comments.
- Text Classification Models
- Train a Classifier (Logistic Regression, SVM, or Random Forest)

Collect high-quality vs. gibberish comments as training data.
Train a binary classifier to detect valid documentation.