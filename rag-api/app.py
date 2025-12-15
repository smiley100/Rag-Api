from fastapi import FastAPI, UploadFile, Form
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import chromadb
import os

app = FastAPI()

# --- URLs des services externes ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

# --- Initialisation du modèle et des embeddings ---
llm = OllamaLLM(model="nemotron-mini:latest", base_url=OLLAMA_URL)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)

# --- Connexion au serveur Chroma via HttpClient ---
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
db = Chroma(client=client, collection_name="documents", embedding_function=embeddings)

# --- Endpoint pour uploader des documents ---
@app.post("/upload")
async def upload_document(file: UploadFile):
    """Ajoute un document PDF ou TXT dans ChromaDB"""
    if not file.filename.endswith((".pdf", ".txt")):
        return {"error": "Seuls les fichiers PDF ou TXT sont acceptés"}

    os.makedirs("/app/data", exist_ok=True)
    filepath = f"/app/data/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(await file.read())

    # --- Chargement du contenu ---
    if file.filename.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
        docs = loader.load()
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            docs = [Document(page_content=text)]

    # --- Découpage en chunks ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # --- Ajout dans Chroma ---
    db.add_documents(chunks)
    os.remove(filepath)

    return {"message": f"{file.filename} ajouté à la base."}

# --- Endpoint pour poser une question ---
@app.post("/ask")
async def ask_question(question: str = Form(...)):
    """Pose une question sur les documents indexés"""
    
    # Récupérer les documents pertinents directement depuis Chroma
    docs = db.similarity_search(question, k=3)

    if not docs:
        return {"response": "Aucun document trouvé pour cette question."}

    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"Réponds à cette question en utilisant le contexte suivant :\n{context}\nQuestion : {question}"

    # Appeler le LLM
    response = llm.invoke(prompt)

    return {"response": response}

# --- Endpoint racine ---
@app.get("/")
def read_root():
    return {"message": "✅ RAG API en ligne et fonctionnelle"}

# --- Lancement Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
