# Global metric list used for aggregation and display.
import re

from sentence_transformers import SentenceTransformer
import torch
_DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer("all-MiniLM-L6-v2", device=str(_DEVICE))


METRICS_LIST = [
    "comment_density",
    "completeness",
    "conciseness",
    "accuracy",
    "overall_score"
]

DOC_TAG_PATTERN = re.compile(
    r"""
    ^\s*(
        :param       |
        :returns?    |
        :raises?     |
        :rtype       |
        Example[s]?: |
        Parameters   |
        Returns      |
        Raises       |
        Args         |
        Kwargs       |
        Yields       |
        Attributes   |
        @param       |
        @return      |
        @raises      |
        @rtype       |
        >>>
    )
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE
)
debug = False


def trim_file_path(file_path: str) -> str:
    """
    Trim the file path to begin from the 'data/' directory if present.

    :param file_path: Original file path.
    :return: Trimmed file path.
    """
    normalized_path = file_path.replace("\\", "/")
    match = re.search(r'data/.*', normalized_path)
    return match.group(0) if match else file_path
