from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os 

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = OpenAIEmbeddings()
vector_store = Chroma(persist_directory= "./chroma_db" , embedding_function=embeddings)

def load_and_split_documents(filepath:str):
    if filepath.endswith('.pdf'):
        loader = PyPDFLoader(filepath)

    elif filepath.endswith('.docx'):
        loader = Docx2txtLoader(filepath)
    
    elif filepath.endswith('.html'):
        loader = UnstructuredHTMLLoader(filepath)

    else:
        raise ValueError(f"Unsupported file path: {filepath}, supported file paths are: '.pdf,' '.docx,' '.html'")
    
    docs = loader.load()
    return text_splitter.split_documents(docs,embeddings)

def index_document_to_chroma(filepath:str, file_id:int):

    try:
        splits = load_and_split_documents(filepath=filepath)

        for split in splits:
            split.metadata['file_id'] = file_id

        vector_store.add_documents(splits)
        return True 
    
    except Exception as e:
        print(f"error indexing {splits} : {e}")
        return False
    
def delete_document_from_chroma(file_id:int):
    try:
        docs = vector_store.get(where={"file_id":file_id})
        print(f"Found {len(docs['ids'])} documents chunks for file_id: {file_id}")

        vector_store._collection.delete(where={"file_id" : file_id})
        print(f"Deleted all documents with file_id: {file_id}")

        return True
    except Exception as e:
        print(f"failed to delete documents with file_id: {file_id} : {e}")
        return False
    
