# RAG API (Retrieval-Augmented Generation) ✨

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
# depuis la machine hôte, si tu as ollama local
ollama list
# ou depuis le conteneur Docker Ollama
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

---

## 🤝 Contribuer

- Propose des améliorations via des PRs (tests, UI, authentification, ingestion de formats supplémentaires).
- Si tu veux, je peux ajouter une petite suite de tests smoke (script qui vérifie `/` et une requête `/ask`) et/ou une action GitHub pour vérifier qu'une instance Ollama contient bien les modèles.

---

## Licence

Pas de licence spécifiée — ajoute un fichier `LICENSE` si tu souhaites en définir une (MIT / Apache 2.0 …).

---

Si tu veux que j'ajoute des badges, une version bilingue FR/EN, des exemples Postman ou une petite action GitHub pour vérifier la présence des modèles, dis‑moi ce que tu préfères et je m'en occupe.