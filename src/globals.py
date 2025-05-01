import re
# Global metric list used for aggregation and display.
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
