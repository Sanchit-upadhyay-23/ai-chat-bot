# AI Chatbot: Resume-Based Q&A

Ask questions like “What is my Name ?” from a resume PDF using local LLMs.

## ⚙️ Tech Stack
git add README.md

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Embeddings**: SentenceTransformers
- **Vector Store**: ChromaDB
- **LLM**: LLaMA 3 via Ollama

##  Setup

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


# How to Run the Project
Start the Ollama server:
ollama serve

Load a Language Model:
ollama run zephyr

Start the FastAPI backend: From the project root directory
uvicorn backend.main:app --reload --port 8000

Start the Streamlit frontend:
cd frontend
streamlit run streamlit_app.py
