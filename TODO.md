### **Comment Density**
- Ignore `from` and `import` statements when calculating comment density.
- Only count inline comments for comment density.
- Exclude class and method declarations from the calculation to separate the metric from completeness.

### **Redundancy**
- Ensure redundancy is not lowered by parameter/return type annotations.
- Likely should not evaluate docstrings at all.
- Consider exploring redundancy among comments (before was redundancy to code).
  - Might be an unexplored area.
  - May not be highly relevant for human-written code, but could be for AI-generated code.

### **Completeness**
- Change completeness to only check for:
  - Parameters (`@param`)
  - Return types (`@return`)
  - A general description.

### **Conciseness**
- Appears to be working well but requires further testing.

### **Readability/Accuracy**
- Currently iffy.
- Likely requires NLP-based improvements.
