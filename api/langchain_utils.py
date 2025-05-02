from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vector_store

base_retriever = vector_store.as_retriever(search_keargs={"k":2})

output_parser=StrOutputParser()

rewrite_query_system_template = (
    
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."

)

rewrite_query_prompt = ChatPromptTemplate.from_messages([
    ("system", rewrite_query_system_template),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def rag_chain(model="gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    history_aware_retriever = create_history_aware_retriever(llm=llm,prompt=rewrite_query_prompt,retriever=base_retriever)
    qa_chain = create_stuff_documents_chain(llm,qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever,qa_chain)
    return rag_chain