# backend/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from backend.rag_engine import embed_documents, query_docs, generate_answer, reset_collection
import fitz  # PyMuPDF
import os

app = FastAPI()
DOC_STORE = []

class QueryInput(BaseModel):
    query: str

def split_into_chunks(text, chunk_size=500, overlap=50):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith(".txt"):
        text = content.decode("utf-8")
    elif file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(content)
        doc = fitz.open("temp.pdf")
        text = "\n".join([page.get_text() for page in doc])
        os.remove("temp.pdf")
    else:
        return {"error": "Unsupported file type"}



    # Clear old data
    reset_collection()
    DOC_STORE.clear()

    chunks = split_into_chunks(text)

    DOC_STORE.extend(chunks)
    embed_documents(chunks)
    return {"status": "Document uploaded"}
@app.get("/documents")
async def list_docs():
    return {"documents": DOC_STORE}

@app.post("/query")
async def ask(input: QueryInput):
    top_chunks = query_docs(input.query, threshold=0.45)

    answer = generate_answer(input.query, top_chunks)
    return {"answer": answer}
