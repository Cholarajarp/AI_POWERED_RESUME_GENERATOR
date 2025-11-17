from fastapi import APIRouter

router = APIRouter()

@router.post("/parse")
async def parse_job(text: str):
    # Simple keyword extraction demo — in production use NLP
    words = [w.strip('.,') for w in text.split() if len(w) > 3][:50]
    keywords = list(dict.fromkeys(words))
    return {"keywords": keywords}
