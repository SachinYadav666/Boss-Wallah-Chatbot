import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")
client = Groq(api_key=groq_api_key)

def create_retriever():
    """
    Loads data, creates embeddings, and builds a FAISS vector store retriever.
    """
    # 1. Load data
    courses_df = pd.read_csv("data/courses.csv")
    lang_map_df = pd.read_csv("data/lang_map.csv")
    
    # 2. Map language codes to names for better context
    lang_map_dict = dict(zip(lang_map_df['Code'], lang_map_df['Language']))
    courses_df['Course Released Languages'] = courses_df['Course Released Languages'].apply(
        lambda x: ', '.join([lang_map_dict.get(int(code.strip()), 'Unknown') for code in str(x).split(',')])
    )
    
    # 3. Create a combined text field for comprehensive context
    courses_df['combined_text'] = courses_df.apply(
        lambda row: f"Course Title: {row['Course Title']}. About Course: {row['About Course']}. Languages: {row['Course Released Languages']}. Audience: {row['Who This Course Is For']}.",
        axis=1
    )
    
    # 4. Load data into LangChain documents
    loader = DataFrameLoader(courses_df, page_content_column='combined_text')
    documents = loader.load()

    # 5. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 6. Create embeddings
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # 7. Create FAISS vector store and retriever
    vectorstore = FAISS.from_documents(texts, embeddings)
    retriever = vectorstore.as_retriever()
    
    return retriever

def get_rag_response(retriever, query: str) -> str:
    """
    Performs the full RAG process: retrieves context, then generates a Groq response.
    """
    try:
        # 1. Retrieve relevant documents based on the user's query
        docs = retriever.get_relevant_documents(query)
        
        # 2. Combine the retrieved documents into a single context string
        context = " ".join([doc.page_content for doc in docs])
        
        # 3. Get the final answer from Groq using the query and context
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Boss Wallah courses. Use the provided context to answer questions about courses. If the information isn't in the context, state that you can only answer based on the provided data."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the Groq API: {e}"
    
    
def get_llm_response(query):
    """
    Performs the full RAG process: retrieves context, then generates a Groq response.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful  Ai assistant made by Boss Wallah ."},
                {"role": "user", "content": f"Question: {query}"}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the Groq API: {e}"