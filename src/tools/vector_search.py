"""
This file contains the vector search tool.

It is responsible for searching for files matching a query using fuzzy matching.
"""
import os
from pathlib import Path
from rapidfuzz import fuzz

from src.tools.directory_manager import directory_manager
from src.utils.config import config


def search(query: str, top_k: int = None):
    """
    Perform a fuzzy search for files matching the given query.

    This function searches through all configured directories and their
    subdirectories for files whose names partially match the search query.
    The matching is performed using fuzzy string matching algorithm from
    the rapidfuzz library, which allows for typos and partial matches.

    Args:
        query (str): The search text to match against filenames
        top_k (int, optional): The maximum number of results to return.
                              If None, uses the value from config.DEFAULT_SEARCH_RESULTS.

    Returns:
        list[str]: A list of absolute file paths ordered by match quality (best matches first).
                  Returns empty list if no matches found above the threshold.

    Note:
        - The match threshold is controlled by config.FUZZY_SEARCH_THRESHOLD (0-100)
        - Only searches directories configured in the directory_manager
        - Matching is case-insensitive

    Example:
        >>> search("config")
        ['/path/to/config.py', '/another/path/config.json']
    """
    if top_k is None:
        top_k = config.DEFAULT_SEARCH_RESULTS

    threshold = config.FUZZY_SEARCH_THRESHOLD
    candidates = []

    for root_alias in directory_manager.directories.values():
        for root, _, files in os.walk(root_alias):
            for f in files:
                score = fuzz.partial_ratio(query.lower(), f.lower())
                if score > threshold:
                    candidates.append((score, str(Path(root) / f)))

    candidates.sort(reverse=True)  # higher score first
    return [p for _, p in candidates[:top_k]]
