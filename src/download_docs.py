"""Download Confluent Kafka documentation starting from the overview page.

This script crawls the Confluent Kafka documentation beginning at
``https://docs.confluent.io/platform/current/overview.html``. It follows
internal links within the same documentation set and stores the HTML locally
mirroring the site structure. The files are later processed and embedded into a
vector database for Retrieval-Augmented Generation (RAG).
"""

from __future__ import annotations

from collections import deque
import logging
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

RAW_DIR = Path("data/raw")
LOG_FILE = Path("data/download.log")
START_URL = "https://docs.confluent.io/platform/current/overview.html"
BASE_PREFIX = "https://docs.confluent.io/platform/current/"
MAX_DEPTH = int(os.getenv("MAX_DEPTH", "3"))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def fetch(url: str) -> str:
    """Return the text content of *url* raising an error for bad responses."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def save_content(content: str, url: str) -> Path:
    """Save *content* under RAW_DIR mirroring the remote path structure."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    filepath = RAW_DIR / path
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    return filepath


def discover_links(html: str, base: str) -> set[str]:
    """Return all internal documentation links found in *html*."""
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]
        url = urljoin(base, href)
        if url.startswith(BASE_PREFIX) and url.endswith(".html"):
            links.add(url)
    return links


def crawl(start_url: str, max_depth: int = MAX_DEPTH) -> None:
    """Crawl documentation starting from *start_url* up to *max_depth* levels."""
    queue: deque[tuple[str, int]] = deque([(start_url, 0)])
    visited: set[str] = set()
    while queue:
        url, depth = queue.popleft()
        if url in visited or depth > max_depth:
            continue
        logger.info("Fetching %s (depth %s)", url, depth)
        try:
            html = fetch(url)
        except requests.RequestException as exc:
            logger.error("Failed to fetch %s: %s", url, exc)
            continue
        filepath = save_content(html, url)
        logger.info("Saved %s", filepath)
        visited.add(url)
        if depth < max_depth:
            for link in discover_links(html, url):
                if link not in visited:
                    queue.append((link, depth + 1))


def main() -> None:
    crawl(START_URL)


if __name__ == "__main__":
    main()
