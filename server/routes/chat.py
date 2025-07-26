from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os
from dotenv import load_dotenv

##Loading dotenv for retrieval of API keys
load_dotenv()

router = APIRouter()

@router.post("/chat/")
async def chat(query:str=Form(...)):
    try:
        logger.info(f"User query: {query}")

        ##Retrieve from pinecone
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

        ##Embed_query
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        embedded_query = embed_model.embed_query(query)

        ##Retrieval
        res = index.query(vector=embedded_query, top_k=5, include_metadata=True)
        docs = [Document(page_content=match.metadata.get("text", ""),\
                       metadata=match["metadata"]
                       ) for match in res["matches"]]


        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self._docs

        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, query)

        logger.info("Query is succesfull")

        return result
    except Exception as e:
        logger.exception("Error in processing query")
        return JSONResponse(status_code=500, content={"error": str(e)})