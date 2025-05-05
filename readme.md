# RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that leverages OpenAI's language models, LangChain, FastAPI, and ChromaDB to provide context-aware responses based on user-uploaded documents. This application supports various document formats and maintains conversational context for enhanced interactions.

---

## 🚀 Features

- **Document Upload & Indexing**: Supports `.pdf`, `.docx`, and `.html` files.
- **Vector-Based Retrieval**: Utilizes embeddings for efficient document retrieval.
- **Conversational Memory**: Maintains context across user interactions.
- **LLM-Powered Responses**: Generates answers using OpenAI's GPT models.
- **FastAPI Backend**: Provides clean and efficient API routes.

---

## 🧠 Architecture Overview

```
User Query
   ↓
FastAPI Endpoint
   ↓
LangChain RAG Chain
   ↓
Retriever (ChromaDB)
   ↓
Relevant Document Chunks
   ↓
OpenAI Chat Model
   ↓
Generated Response
```

---

## 🛠️ Tech Stack

- **Programming Language**: Python 3.10+
- **Frameworks & Libraries**:
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [LangChain](https://www.langchain.com/)
  - [OpenAI API](https://platform.openai.com/docs)
  - [ChromaDB](https://www.trychroma.com/) (or FAISS as an alternative)
  - Document Loaders: `PyPDF2`, `python-docx`, `html.parser`
- **Frontend**: [Streamlit](https://streamlit.io/) for interactive UI

---

## 📂 Project Structure

```
RAG-Chatbot/
├── api/                     # FastAPI backend modules
├── app/                     # Streamlit frontend application
├── chroma_db/               # Directory for ChromaDB storage
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/BhavyaJethwa/RAG-Chatbot.git
cd RAG-Chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the FastAPI Backend

```bash
uvicorn api.main:app --reload
```

### 6. Launch the Streamlit Frontend

In a new terminal window:

```bash
streamlit run app/main.py
```

Access the application at `http://localhost:8501`.

---

## 📄 Usage

1. **Upload Documents**: Use the Streamlit interface to upload `.pdf`, `.docx`, or `.html` files.
2. **Ask Questions**: Enter your queries in the chat interface.
3. **Receive Answers**: The chatbot retrieves relevant information from the uploaded documents and provides context-aware responses.

---

## 🧪 Example

*User*: "What is the main topic of the uploaded document?"

*Chatbot*: "The document primarily discusses the impact of climate change on coastal ecosystems, highlighting the rising sea levels and increased storm frequency."

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://streamlit.io/)