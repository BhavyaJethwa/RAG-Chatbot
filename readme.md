# 📚 RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot using OpenAI, LangChain, FastAPI, and a vector store (ChromaDB/FAISS). It can answer user queries based on uploaded documents, maintaining conversational context.

---

## 🔧 Features

- 📄 Upload and index documents (`.pdf`, `.docx`, `.html`)
- 🧠 Vector-based document retrieval using embeddings
- 🗣️ Conversational memory (context-aware question reformulation)
- 🤖 LLM-powered answers using OpenAI (gpt-4o / gpt-4o-mini)
- 🚀 FastAPI backend with clean API routes

---

## 🏗️ Architecture Overview

```
User → FastAPI → LangChain RAG Chain → Retriever (ChromaDB) → Documents
                                          ↓
                                   OpenAI Chat Model
                                          ↓
                                      Response
```

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI
- LangChain
- OpenAI API (ChatGPT models)
- ChromaDB (or FAISS for vector storage)
- PyPDF / python-docx / html parser (for document ingestion)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

### 4. Run the app

```bash
uvicorn app:app --reload
```

---

## 📁 API Endpoints

| Method | Endpoint           | Description                        |
|--------|--------------------|------------------------------------|
| POST   | `/upload-doc`      | Upload and index a document        |
| GET    | `/list-docs`       | List all uploaded documents        |
| POST   | `/ask`             | Ask a question (chat interface)    |
| DELETE | `/delete-doc/{id}` | Delete a specific document         |

---

## 📤 Example Query Payload

```json
POST /ask
{
  "question": "What is the refund policy?",
  "session_id": "abc123",
  "model": "gpt-4o"
}
```

---

## 🧠 How It Works

1. Uploaded documents are parsed and embedded using OpenAI's embeddings.
2. Embeddings are stored in a vector database (e.g., ChromaDB).
3. When a user asks a question:
   - The chatbot uses `create_history_aware_retriever` to rewrite the question (if necessary).
   - Relevant documents are retrieved using vector similarity.
   - The LLM uses the context to answer the question.
4. Chat history is preserved via session IDs for contextual continuity.

---
