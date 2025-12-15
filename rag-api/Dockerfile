# ---- Image de base ----
FROM python:3.11-slim

# ---- Répertoire de travail ----
WORKDIR /app

# ---- Copie des fichiers de dépendances ----
COPY requirements.txt .

# ---- Installation des dépendances ----
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -U \
        langchain \
        langchain-chroma \
        langchain-ollama \
        langchain-community \
        chromadb \
        pypdf

# ---- Copie du code ----
COPY . .

# ---- Commande de démarrage ----
CMD ["python", "app.py"]
