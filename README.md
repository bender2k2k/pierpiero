# pierpiero

Applicazione RAG per la documentazione Confluent Kafka.

## Clonare il repository

### Da riga di comando
1. Assicurarsi di avere [Git](https://git-scm.com/) installato sul proprio sistema.
2. Clonare il progetto:
   ```bash
   git clone https://github.com/<tuo-utente>/pierpiero.git
   ```
3. Entrare nella cartella del progetto:
   ```bash
   cd pierpiero
   ```

### Con Visual Studio Code
1. Aprire VS Code.
2. Aprire la Command Palette (`Ctrl+Shift+P` su Windows/Linux, `Cmd+Shift+P` su macOS).
3. Selezionare **Git: Clone** e incollare l'URL del repository `https://github.com/<tuo-utente>/pierpiero.git`.
4. Scegliere la cartella di destinazione in cui salvare il progetto.
5. Al termine, VS Code propone di aprire la cartella clonata; confermare per iniziare a lavorare sul codice.

## Struttura

- `src/download_docs.py` – scarica la documentazione a partire dall'overview seguendo i link interni, loggando su schermo e su `data/download.log`.
- `src/ingest.py` – estrae il testo e popola un database vettoriale Chroma.
- `src/app.py` – espone un endpoint FastAPI per rispondere alle domande usando RAG.
- `requirements.txt` – dipendenze Python.
- `Dockerfile` – containerizzazione dell'applicazione.

## Utilizzo

1. Installare le dipendenze: `pip install -r requirements.txt`.

2. Scaricare la documentazione: `python src/download_docs.py`. La profondità di esplorazione può essere impostata con `MAX_DEPTH` (default `3`) e il progresso è visibile anche nel file `data/download.log`.
3. Ingerire i documenti: `python src/ingest.py`.
4. Avviare l'API: `uvicorn src.app:app --reload`, interrogare `POST /query` con `{ "question": "..." }`
   oppure aprire `GET /` per utilizzare una semplice interfaccia web.

### Docker

```bash
docker build -t confluent-rag .
docker run -p 8000:8000 -e OPENAI_API_KEY=yourkey confluent-rag
```
