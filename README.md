# pierpiero

Applicazione RAG per la documentazione Confluent Kafka.

## Struttura


- `src/download_docs.py` – scarica la documentazione a partire dall'overview seguendo i link interni.

- `src/ingest.py` – estrae il testo e popola un database vettoriale Chroma.
- `src/app.py` – espone un endpoint FastAPI per rispondere alle domande usando RAG.
- `requirements.txt` – dipendenze Python.
- `Dockerfile` – containerizzazione dell'applicazione.

## Utilizzo

1. Installare le dipendenze: `pip install -r requirements.txt`.
2. Scaricare la documentazione: `python src/download_docs.py`.
3. Ingerire i documenti: `python src/ingest.py`.
4. Avviare l'API: `uvicorn src.app:app --reload`, interrogare `POST /query` con `{ "question": "..." }`
   oppure aprire `GET /` per utilizzare una semplice interfaccia web.

### Docker

```bash
docker build -t confluent-rag .
docker run -p 8000:8000 -e OPENAI_API_KEY=yourkey confluent-rag
```
