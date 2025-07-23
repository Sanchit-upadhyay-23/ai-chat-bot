# backend/rag_engine.py
import os
# from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient

from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

embed_model = SentenceTransformer("all-mpnet-base-v2", device="cpu")


llm = OllamaLLM(
    model="llama3:8b-instruct-q4_K_M",
    temperature=0.7,
    num_predict=256
)

hf_token = os.getenv("HUGGINGFACE_TOKEN")

# Setup Chroma
chroma_client = PersistentClient(path=".chromadb")
collection = chroma_client.get_or_create_collection("docs")


def reset_collection():
    # Properly reset collection by deleting and recreating with correct embedding dimension
    try:
        chroma_client.delete_collection("docs")
    except Exception:
        pass  # collection may not exist yet

    global collection
    collection = chroma_client.get_or_create_collection("docs")


def embed_documents(docs):
    embeddings = embed_model.encode(docs)
    ids = [f"doc_{i}" for i in range(len(docs))]
    collection.add(documents=docs, embeddings=embeddings, ids=ids)

def query_docs(question, threshold=0.4):
    q_embed = embed_model.encode([question])[0]
    results = collection.query(query_embeddings=[q_embed], n_results=10)
    
    docs = results["documents"][0]
    if not docs:
        return []

    pairs = [[question, doc] for doc in docs]
    scores = reranker.predict(pairs)
    ranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)]
    
    return ranked_docs[:3]  # return top 3 reranked


def generate_answer(question, context_chunks):
    context = "\n---\n".join(context_chunks)
    prompt = f"""
Extract the exact answer from the context below. Do not assume or guess.

Context:
{context}

Question: {question}

Answer:"""
    return llm.invoke(prompt.strip())



