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

## Utilizzo manuale

1. Installare le dipendenze: `pip install -r requirements.txt`.
2. Scaricare la documentazione: `python src/download_docs.py`. La profondità di esplorazione può essere impostata con `MAX_DEPTH` (default `3`) e il progresso è visibile anche nel file `data/download.log`.
3. Ingerire i documenti: `python src/ingest.py`.
4. Avviare l'API: `uvicorn src.app:app --reload`, interrogare `POST /query` con `{ "question": "..." }`
   oppure aprire `GET /` per utilizzare una semplice interfaccia web.

## Esecuzione tramite Docker

### Build dell'immagine

```bash
docker build -t confluent-rag .
```

### Avvio del container

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=yourkey \
  confluent-rag
```

### Scaricare e ingerire la documentazione nel container

Puoi eseguire i comandi direttamente nel container:

```bash
docker run -it --rm \
  -e OPENAI_API_KEY=yourkey \
  confluent-rag /bin/bash
```

All'interno del container:

```bash
python src/download_docs.py
python src/ingest.py
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### Variabili d'ambiente utili

- `OPENAI_API_KEY`: chiave API per l'accesso ai modelli OpenAI.
- `MAX_DEPTH`: profondità di crawling della documentazione (default: `3`).

### Accesso all'applicazione

Una volta avviato il container, l'API sarà disponibile su [http://localhost:8000](http://localhost:8000).

## Note

- I dati scaricati e i log sono salvati nella cartella `data/` del container. Puoi montare una directory locale con `-v $(pwd)/data:/app/data` per persistenza.
- Modifica i parametri di avvio secondo le tue esigenze, consultando la documentazione di Docker e FastAPI se necessario.
