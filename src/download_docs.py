"""Download Confluent Kafka documentation pages.

This script fetches a predefined set of Confluent Kafka documentation
pages and stores the HTML locally. The downloaded files will later be
processed and embedded into a vector database for Retrieval-Augmented
Generation (RAG).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import requests

RAW_DIR = Path("data/raw")

# A small subset of Confluent documentation URLs. Extend this list as needed.
DOC_URLS: Iterable[str] = [
    "https://docs.confluent.io/platform/current/kafka/index.html",
    "https://docs.confluent.io/platform/current/kafka/overview.html",
    "https://docs.confluent.io/platform/current/installation/index.html",
]

def fetch(url: str) -> str:
    """Return the text content of *url* raising an error for bad responses."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

def save_content(content: str, url: str) -> None:
    """Save *content* to RAW_DIR using the last component of *url* as filename."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1] or "index.html"
    (RAW_DIR / filename).write_text(content, encoding="utf-8")

def main() -> None:
    for url in DOC_URLS:
        print(f"Fetching {url}")
        html = fetch(url)
        save_content(html, url)

if __name__ == "__main__":
    main()
