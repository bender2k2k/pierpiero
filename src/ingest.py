"""Ingest downloaded documentation into a Chroma vector database."""

from __future__ import annotations

import glob
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

RAW_DIR = Path("data/raw")
CHROMA_DIR = Path("data/chroma")

def load_documents() -> List[Document]:
    docs: List[Document] = []
    for path in glob.glob(str(RAW_DIR / "*.html")):
        text = Path(path).read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "html.parser")
        content = soup.get_text(separator=" \n")
        docs.append(Document(page_content=content, metadata={"source": path}))
    return docs

def main() -> None:
    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings()
    vectordb = Chroma.from_documents(splits, embeddings, persist_directory=str(CHROMA_DIR))
    vectordb.persist()

if __name__ == "__main__":
    main()
