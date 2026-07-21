import re
from typing import List, Dict, Any


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and stripping extra whitespace."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip().lower())


def contains_any(text: str, keywords: List[str]) -> bool:
    """Check if normalized text contains any of the given keywords."""
    norm = normalize_text(text)
    return any(kw.lower() in norm for kw in keywords)


def extract_numbers(text: str) -> List[str]:
    """Extract numbers from text string."""
    return re.findall(r"\d+(?:\.\d+)?", text)
