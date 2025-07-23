# frontend/streamlit_app.py (in /frontend)
import streamlit as st
import requests

API = "http://localhost:8000"

st.title(" Ask Questions About Your Documents")

st.sidebar.header(" Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or TXT", type=["pdf", "txt"])
if uploaded_file:
    res = requests.post(
        f"{API}/upload-document",
        files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    )
    st.sidebar.success(" Uploaded") if res.status_code == 200 else st.sidebar.error(res.text)

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader(" Ask a Question")
question = st.text_input("Enter your question:")

if question:
    res = requests.post(f"{API}/query", json={"query": question})
    if res.status_code == 200:
        answer = res.json()["answer"]
        st.session_state.history.append((question, answer))
    else:
        st.error(f" Error: {res.text}")

for q, a in st.session_state.history:
    st.markdown(f"** You:** {q}")
    st.markdown(f"** Bot:** {a}")
