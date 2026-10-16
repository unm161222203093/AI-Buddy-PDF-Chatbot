# AI-Buddy-PDF-Chatbot
# AI Buddy PDF Chatbot

A chatbot that answers questions from uploaded PDF documents using a Large Language Model (LLM) and ChromaDB. Built during my Machine Learning internship at Atandra Energy Private Limited.

## How it works
1. The PDF is read and its text is split into small chunks.
2. Each chunk is converted into an embedding and stored in ChromaDB (vector database).
3. When you ask a question, the most relevant chunks are retrieved using semantic search.
4. The LLM uses those chunks to give an accurate answer from the document (RAG approach).

## Tech Stack
- Python
- Large Language Model (LLM)
- ChromaDB (vector database)
- Embeddings

## How to run
1. Clone the repository: `git clone <repo-link>`
2. Install the requirements: `pip install -r requirements.txt`
3. Add your API key in a `.env` file (do not upload this file)
4. Run: `python app.py`

## Author
Keerthana E | MCA Student
[LinkedIn](https://www.linkedin.com/in/keerthana-e-556b72361/)
