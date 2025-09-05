# Boss Wallah Chatbot API

This is a FastAPI-based chatbot API for Boss Wallah courses. It supports:

* **RAG (Retriever + Groq LLM)**: Uses course data to provide answers.
* **LLM-only mode**: Directly queries Groq LLM without using retriever.

---

## 🛠 Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd boss-wallah-chatbot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure your `requirements.txt` includes:

```
fastapi
uvicorn
pandas
faiss-cpu
sentence-transformers
groq
python-dotenv
langchain-community 
langchain-huggingface
numpy==1.26.4
requests 
beautifulsoup4
google-api-python-client
```

### 4. Set up environment variables

Create a `.env` file in the root directory with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Prepare the data

Ensure the following CSV files exist in the `data/` folder:

* `courses.csv` – course details
* `lang_map.csv` – language code mapping

---

## 🚀 Running the API

Start the FastAPI server:

```bash
python main.py
```

Default URL:

```
http://127.0.0.1:8000
```

Interactive Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 📦 API Endpoint

### **POST /chat**

Single endpoint to handle both RAG and LLM queries.

**Request Body (JSON):**

```json
{
  "query": "Your question here",
  "type": "rag"  // optional, default is "rag"; use "llm" for LLM-only
}
```

**Example 1: RAG query (default)**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "Tell me about Python courses"}'
```

**Example 2: LLM-only query**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "Tell me about Python courses", "type": "llm"}'
```

**Response (JSON):**

```json
{
  "query": "Tell me about Python courses",
  "type": "rag",
  "response": "The course Python Basics covers..."
}
```

---

## ⚡ Notes

* The RAG pipeline is **initialized once** at startup for faster responses.
* Ensure your `GROQ_API_KEY` is valid to avoid API errors.
* Use the `type` field to switch between **RAG** and **LLM-only** modes.
