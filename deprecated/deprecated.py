# CodeMetrics.py
# noinspection all
def _embed_batch(texts: list[str]) -> torch.Tensor:
    """
    Generate L2-normalized embeddings for a batch of texts using the UniXcoder model.

    This function tokenizes the input texts, pads them to the same length, and processes
    them through the UniXcoder model. It also applies an attention mask to ensure that
    padding tokens are ignored during processing. The resulting embeddings are normalized
    using L2 normalization.

    :param texts: A list of input strings to embed.
    :return: A PyTorch tensor containing the L2-normalized embeddings for the input texts.
    """
    token_lists = _unixcoder.tokenize(texts, max_length=512, mode="<encoder-only>")
    max_len = max(len(t) for t in token_lists)
    pad_id = getattr(_unixcoder, "pad_id", 1)

    padded = [t + [pad_id] * (max_len - len(t)) for t in token_lists]
    mask = [[1] * len(t) + [0] * (max_len - len(t)) for t in token_lists]  # 1 = real, 0 = pad

    src = torch.tensor(padded, device=_device)
    attn_mask = torch.tensor(mask, device=_device)

    _, emb = _unixcoder(src, attention_mask=attn_mask)  # UniXcoder respects mask
    return torch.nn.functional.normalize(emb, p=2, dim=1)

# CodeMetrics.py
# noinspection all
def extract_comment_code_pairs(source: str) -> List[Tuple[str, str]]:
    lines = source.splitlines()
    pairs = []
    n = len(lines)

    # Get docstring lines using AST
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(source)
        docstring_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                doc = ast.get_docstring(node)
                if doc and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    first_line = node.body[0].lineno - 1
                    docstring_lines.update(range(first_line, first_line + doc.count('\n') + 1))
    except SyntaxError:
        docstring_lines = set()

    def is_hanging_string(line: str) -> bool:
        stripped = line.strip()
        return (
                (stripped.startswith('"') or stripped.startswith("'")) and
                (stripped.endswith('"') or stripped.endswith("'")) and
                not (stripped.startswith('"""') or stripped.startswith("'''")) and
                len(stripped) > 1
        )

    def is_code_line(line: str) -> bool:
        return bool(line.strip()) and not line.strip().startswith("#") and not is_hanging_string(line)

    i = 0
    while i < n - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()

        if i in docstring_lines or (i + 1) in docstring_lines:
            i += 1
            continue

        # comment followed by real code
        if line.startswith("#") and is_code_line(next_line):
            pairs.append((line, next_line))
            i += 2
            continue

        # hanging string comment followed by real code
        if is_hanging_string(line) and is_code_line(next_line):
            pairs.append((line, next_line))
            i += 2
            continue

        i += 1

    return pairs