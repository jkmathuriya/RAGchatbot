# 🤖 Business Assistant Chatbot
An intelligent AI-powered business assistant chatbot that can understand documents, answer queries, and assist with day-to-day business tasks. Powered by LLMs, RAG (Retrieval-Augmented Generation), and vector search.

# 🧱 Tech Stack
🧠 LLM: llama-70b (hosted using groq), Google-gen-ai(embedding-001)\
📚 RAG: LangChain\
📦 Vector Store: Pinecone\
📄 Document Ingestion: PDF, DOCX, CSV support\
🖥️ Backend: FastAPI\
🧑‍💻 Frontend: Streamlit

# 📂 Folder Structure


# ⚙️ How to Use
### 1. Clone the Repo
```bash
##Clone the repo
git clone https://github.com/jkmathuriya/RAGchatbot.git
##Change path
cd RAGchatbot
```
### 2. Install Requirements
```bash
cd server
pip install -r requirements.txt
```
### 3. Set Environment Variables
Create a .env file:
```
GOOGLE_API_KEY="api_key"
GROQ_API_KEY="api_key"
PINECONE_API_KEY="api_key"
PINECONE_INDEX_NAME='index-name'
```
### 4. Run the Backend Server
```bash
cd server
uvicorn main:app --reload
```
### 5. Edit URL in client/config.py & Run client
```
#Edit client/config.py with API_URL with backend URL
cd client
streamlit run app.py
```

# 🧑‍💼 Use Cases
- Internal company knowledge base
- HR policy Q&A bot
- Document search assistant for sales/legal teams
- Personal business assistant for founders/execs


