# RAG API (Retrieval-Augmented Generation) ✨

FRENCH

**Description rapide**

API RAG légère développée avec **FastAPI** qui combine :
- **Ollama** (LLM + embeddings)
- **ChromaDB** (stockage vectoriel)

L'application permet d'uploader des fichiers (PDF/TXT), d'indexer leur contenu et de poser des questions auxquelles le modèle répond en s'appuyant sur les passages les plus pertinents.

---

## 🔧 Prérequis importants

- **Docker** et **Docker Compose** (v2 recommandée) doivent être installés.
- **Mémoire recommandée : 8 GB de RAM** (fonctionne parfois avec moins, mais la qualité/performance peut baisser). 

> Conseil : Si tu manques de RAM, ferme d'autres gros processus et augmente la mémoire disponible pour Docker avant de démarrer.

---

## ✅ Première exécution (très importante)

Pour la première exécution, lance :

```bash
docker compose up -d --build
```

Pourquoi : le service `ollama` est configuré pour démarrer via `scripts/init_ollama.sh` (il démarre le service Ollama et télécharge automatiquement les modèles requis). Lancer `docker compose up -d` la première fois garantit que les volumes sont créés et que le script de démarrage s'exécute correctement.

---

## ⚠️ Modèles Ollama requis

Les modèles suivants doivent être présents dans Ollama pour que l'API fonctionne correctement :

- `nemotron-mini:latest` — modèle LLM de génération
- `nomic-embed-text:latest` — modèle d'embeddings

Le démarrage du service Ollama via `docker compose up -d` exécutera `scripts/init_ollama.sh` (monté dans le conteneur) et **cela télécharge automatiquement ces modèles**. Si tu préfères contrôler le processus manuellement, tu peux utiliser la CLI Ollama (si installée localement) :

Vérifier la présence des modèles (depuis la machine hôte ou depuis le conteneur) :

```bash
docker exec -it ollama ollama list
```

Remarque importante : **Ne modifie pas `scripts/init_ollama.sh`** — il est fourni et configuré pour démarrer Ollama et télécharger les modèles. Le script est déjà exécutable et validé.

---

## 🚀 Endpoints et utilisation basique

Base URL (local) : `http://localhost:5000`

- `GET /` — vérification de santé

Exemple :

```bash
curl http://localhost:5000/
# => {"message":"✅ RAG API en ligne et fonctionnelle"}
```

- `POST /upload` — uploader un PDF ou TXT (multipart/form-data)

Exemple :

```bash
curl -X POST "http://localhost:5000/upload" -F "file=@/chemin/vers/ton_doc.pdf"
```

- `POST /ask` — poser une question (form param `question`)

Exemple :

```bash
curl -X POST "http://localhost:5000/ask" -F "question=Quelle est la capitale du Sénégal ?"
```

Le service récupère les passages les plus similaires via ChromaDB et construit un prompt envoyé au modèle pour générer la réponse.

---

## 📁 Volumes et persistance

- Volume Ollama : `ollama_data` (stocke les modèles)
- Volume ChromaDB : `chroma_data` (indexs persistants)
- Uploads temporaires : `./rag-api/data` (monté dans le conteneur `rag-api`)

---

## 🛠️ Dépannage rapide

- Les modèles ne sont pas disponibles : vérifie `docker logs ollama` et/ou lance `docker exec -it ollama ollama list`.
- L'API renvoie une erreur liée à Ollama : vérifie que `OLLAMA_URL` (dans la config/dans l'environnement du conteneur `rag-api`) pointe bien sur `http://ollama:11434`.
- Pour voir les logs :

```bash
docker-compose logs -f rag-api
docker-compose logs -f chromadb
docker-compose logs -f ollama
```

## Licence

Pas de licence spécifiée 

ENGLISH

Bien sûr. Voici la **version anglaise fidèle et propre**, prête à être utilisée telle quelle dans ton README 👌

---

# RAG API (Retrieval-Augmented Generation) ✨

**Quick description**

A lightweight RAG API built with **FastAPI** that combines:

* **Ollama** (LLM + embeddings)
* **ChromaDB** (vector storage)

The application allows you to upload documents (PDF/TXT), index their content, and ask questions answered by the model using the most relevant retrieved passages.

---

## 🔧 Important prerequisites

* **Docker** and **Docker Compose** (v2 recommended) must be installed.
* **Recommended memory: 8 GB of RAM** (it may run with less, but performance and quality can degrade).

> Tip: If you are low on RAM, close heavy applications and increase the memory available to Docker before starting.

---

## ✅ First run (very important)

For the first execution, run:

```bash
docker compose up -d --build
```

Why: Running `docker exec -it ollama /bin/sh /scripts/init_ollama.sh`  ensures required models are correctly been downloaded in ollama container.

---

## ⚠️ Required Ollama models

The following models must be available in Ollama for the API to work properly:

* `nemotron-mini:latest` — LLM for text generation
* `nomic-embed-text:latest` — embedding model


If you prefer to check manually, you can use the Ollama CLI:

```bash
docker exec -it ollama ollama list
```

Important note: **Do not modify `scripts/init_ollama.sh`**. It is provided and configured to start Ollama and pull the required models.

---

## 🚀 Endpoints and basic usage

Base URL (local): `http://localhost:5000`

* `GET /` — health check

Example:

```bash
curl http://localhost:5000/
# => {"message":"✅ RAG API is up and running"}
```

* `POST /upload` — upload a PDF or TXT file (multipart/form-data)

Example:

```bash
curl -X POST "http://localhost:5000/upload" -F "file=@/path/to/your_doc.pdf"
```

* `POST /ask` — ask a question (form parameter `question`)

Example:

```bash
curl -X POST "http://localhost:5000/ask" -F "question=What is the capital of Senegal?"
```

The service retrieves the most relevant chunks from ChromaDB and builds a prompt sent to the LLM to generate the answer.

---

## 📁 Volumes and persistence

* Ollama volume: `ollama_data` (stores models)
* ChromaDB volume: `chroma_data` (persistent vector indexes)
* Temporary uploads: `./rag-api/data` (mounted inside the `rag-api` container)

---

## 🛠️ Quick troubleshooting

* Models not available: check `docker logs ollama` or run `docker exec -it ollama ollama list`.
* API errors related to Ollama: ensure `OLLAMA_URL` (in the `rag-api` container environment) points to `http://ollama:11434`.
* View logs:

```bash
docker compose logs -f rag-api
docker compose logs -f chromadb
docker compose logs -f ollama
```

---

## License

No license specified 
