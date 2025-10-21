from fastapi import FastAPI, UploadFile, Form
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import os


app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHROMA_PATH = "/app/chroma_db"

# --- Initialisation du modèle LLM et des embeddings ---
llm = Ollama(model="mistral:7b", base_url=OLLAMA_URL)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)

# --- Initialisation de la base vectorielle Chroma ---
if not os.path.exists(CHROMA_PATH):
    os.makedirs(CHROMA_PATH)

db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever(search_kwargs={"k": 3}))

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Ajoute un document PDF ou TXT dans ChromaDB"""
    filepath = f"/app/data/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(filepath)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    db.add_documents(chunks)
    db.persist()

    if os.path.exists(filepath):
        os.remove(filepath)
    return {"message": f"{file.filename} ajouté à la base."}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    """Pose une question sur les documents indexés"""
    response = qa_chain.run(question)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
