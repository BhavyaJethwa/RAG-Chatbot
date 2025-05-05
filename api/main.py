from fastapi import FastAPI, File, UploadFile, HTTPException
from db_utils import insert_application_logs, insert_document_record, delete_document_record, get_all_documents, get_chat_history
from chroma_utils import index_document_to_chroma, delete_document_from_chroma
from langchain_utils import rag_chain
from pydantic_model import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
import os
import shutil
import uuid
import logging 
logging.basicConfig(filename='app.log', level = logging.INFO)
app = FastAPI()

#from fastapi import FastAPI, File, UploadFile, HTTPException
@app.post("/upload-doc")
def upload_and_index_document(file:UploadFile = File(...)):
    allowed_extension = ['.pdf','.docx', '.html']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extension:
        raise HTTPException(status_code=400, detail=f"Unsupported file type, supported file types are: {', '.join(allowed_extension)}")
    
    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path,'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        print("Document inserted successfully")
        success = index_document_to_chroma(temp_file_path,file_id)

        if success:
            return {"message" : f"{file} successfully uploaded and indexed" , "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/delete-doc")
def delete_document(request:DeleteFileRequest):
    chroma_delete_success = delete_document_from_chroma(request.file_id)
    
    if chroma_delete_success:
        db_delete_success = delete_document_record(request.file_id)

        if db_delete_success:
            return {"message" : f"Successfully deleted document with file_id: {request.file_id}."}
        else:
            return {"message" : f"Failed to delete document with file_id: {request.file_id}."}

    else:
        return {"ERROR" : f"Failed to delete the document with file_id: {request.file_id} from Chroma."}
    

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(f"session_id: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

    if not session_id:
        session_id = str(uuid.uuid4())

    chat_history = get_chat_history(session_id=session_id)
    rag = rag_chain()  # avoid variable shadowing
    answer = rag.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    })['answer']

    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    logging.info(f"session_id: {session_id}, AI Response: {answer}")

    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

from typing import List
@app.get("/list-docs" , response_model = List[DocumentInfo])
def list_document():
    return get_all_documents()



