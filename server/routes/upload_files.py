
from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_doc import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

router = APIRouter()


@router.post("/upload_files/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        logger.info("Received uploaded files")
        load_vectorstore(files)
        logger.info("Document added to vector store")
        return JSONResponse(status_code=200, content={"message": "Files stored and vector store updated"})
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500, content={"error": str(e)})
