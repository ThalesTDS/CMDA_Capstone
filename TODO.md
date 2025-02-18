### **Comment Density**
- Ignore `from` and `import` statements when calculating comment density.
- Only count inline comments for comment density.
- Exclude class and method declarations from the calculation to separate the metric from completeness.

### **Conciseness**
- Appears to be working well but requires further testing.

### **Readability/Accuracy**
- Currently iffy.
- Likely requires NLP-based improvements.

### **Completeness** 
- Currently returns a bools
- Needs to return a float.
- Im going to work on that -Amy

### **General**
- Create/Find sample code to run tests on.
- Adjust weighting of metrics.