# 🧠 AI Chatbot: Resume-Based Q&A

Ask questions like “What is my CGPA?” from a resume PDF using local LLMs.

## ⚙️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Embeddings**: SentenceTransformers
- **Vector Store**: ChromaDB
- **LLM**: LLaMA 3 via Ollama

## 🚀 Setup

```bash
# 1. Clone the repo
git clone https://github.com/Sanchit-upadhyay-23/ai-chat-bot.git
cd ai-chat-bot

# 2. Create a virtualenv and activate
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the model
ollama pull llama3:8b-instruct-q4_K_M

# 5. Start the backend
uvicorn backend.main:app --reload

# 6. Start the frontend
streamlit run frontend/app.py
