"""FastAPI application exposing a simple RAG endpoint."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

CHROMA_DIR = "data/chroma"

app = FastAPI(title="Confluent Kafka RAG")

class Query(BaseModel):
    question: str

@app.on_event("startup")
def startup() -> None:
    global qa_chain
    embeddings = HuggingFaceEmbeddings()
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    llm = OpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever())

@app.post("/query")
def query(data: Query) -> dict[str, str]:
    try:
        answer = qa_chain.run(data.question)
        return {"answer": answer}
    except Exception as exc:  # pragma: no cover - broad catch for API stability
        raise HTTPException(status_code=500, detail=str(exc))
