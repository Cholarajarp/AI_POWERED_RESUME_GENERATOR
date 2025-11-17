from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from ..ai.ai_client import ai_client

router = APIRouter()

sessions = {}

@router.post("/session/create")
async def create_session(payload: dict):
    # payload: {role, difficulty, language}
    sid = str(uuid4())
    sessions[sid] = {"role": payload.get("role"), "difficulty": payload.get("difficulty"), "q_index": 0}
    return {"id": sid}

@router.post("/session/{id}/next_question")
async def next_question(id: str):
    s = sessions.get(id)
    if not s:
        return {"error": "session not found"}
    # generate a question using ai_client (stubbed)
    q = {"id": f"q{ s['q_index'] }", "text": f"Sample question for role {s['role']} (difficulty {s['difficulty']})"}
    s['q_index'] += 1
    return {"question": q}

@router.post("/session/{id}/submit_answer")
async def submit_answer(id: str, answer: str = ""):
    s = sessions.get(id)
    if not s:
        return {"error": "session not found"}
    # evaluate answer
    eval_res = await ai_client.call(f"Evaluate answer: {answer}")
    return {"evaluation": eval_res}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # TODO: integrate whisper or fallback
    content = await file.read()
    return {"transcript": "(simulated) transcribed text"}

@router.post("/evaluate")
async def evaluate(payload: dict):
    # payload: {transcript, question}
    resp = await ai_client.call(f"Evaluate transcript: {payload.get('transcript')}")
    return {"result": resp}
