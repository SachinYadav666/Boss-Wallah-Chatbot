from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from src.rag_pipeline import create_retriever, get_rag_response, get_llm_response

# Initialize FastAPI
app = FastAPI()

# Pydantic model for request body
class ChatRequest(BaseModel):
    query: str
    type: str = "rag"  # Default is "rag"; if "llm", use LLM directly

# Initialize the RAG pipeline once
print("Initializing RAG pipeline...")
retriever = create_retriever()
print("RAG pipeline initialized successfully.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Boss Wallah Chatbot API! Use the /chat endpoint to get started."}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Single POST endpoint that chooses between RAG or LLM based on request type.
    """
    try:
        if request.type.lower() == "llm":
            # Use LLM only
            answer = get_llm_response(request.query)
        else:
            # Use RAG retriever + LLM
            answer = get_rag_response(retriever, request.query)
        
        return {"query": request.query, "type": request.type, "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
