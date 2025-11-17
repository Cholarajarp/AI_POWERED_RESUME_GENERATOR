from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..ai.ai_client import AIClient
from ..core.config import settings

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # TODO: store to MinIO and create Resume record
    content = await file.read()
    # naive text extraction for demo
    text = content.decode(errors="ignore")[:1000]
    return JSONResponse({"filename": file.filename, "extracted_preview": text})

@router.post("/extract")
async def extract_resume():
    # TODO: extract text from stored resume
    return {"extracted": "TODO"}

@router.post("/rewrite")
async def rewrite_resume():
    # TODO: call AIClient with resume rewrite prompt
    return {"rewritten": "TODO"}

@router.get("/download")
async def download_resume():
    # TODO: stream file from MinIO
    raise HTTPException(status_code=501, detail="Not implemented")
