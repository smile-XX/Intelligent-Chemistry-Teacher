"""
AI 化学老师 V1 - FastAPI 主应用
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .database import init_db, save_wrong_question, list_wrong_questions, get_wrong_question, delete_wrong_question
from .llm_service import call_llm

app = FastAPI(title="AI 化学老师 V1", description="高中化学 AI 提分讲解 + 错题本系统", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

FRONTEND_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "frontend"

@app.get("/")
def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/wrong.html")
def serve_wrong():
    return FileResponse(FRONTEND_DIR / "wrong.html")

@app.get("/detail.html")
def serve_detail():
    return FileResponse(FRONTEND_DIR / "detail.html")

class Question(BaseModel):
    question: str

class SaveWrongRequest(BaseModel):
    question: str
    tags: str = ""

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AI 化学老师 V1 已运行"}

@app.post("/api/explain")
def explain_question(q: Question):
    if not q.question.strip():
        raise HTTPException(status_code=400, detail="请输入化学题目")
    answer = call_llm(q.question)
    return {"question": q.question, "answer": answer}

@app.post("/api/wrong/save")
def save_wrong(req: SaveWrongRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="题目不能为空")
    answer = call_llm(req.question)
    question_id = save_wrong_question(req.question, answer, req.tags)
    return {"status": "ok", "id": question_id, "answer": answer}

@app.get("/api/wrong/list")
def list_wrong():
    return {"questions": list_wrong_questions()}

@app.get("/api/wrong/{question_id}")
def get_wrong(question_id: int):
    question = get_wrong_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="错题不存在")
    return question

@app.delete("/api/wrong/{question_id}")
def delete_wrong(question_id: int):
    deleted = delete_wrong_question(question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="错题不存在")
    return {"status": "ok", "message": "已删除"}

@app.on_event("startup")
def on_startup():
    init_db()
    print("[OK] 数据库初始化完成 | 访问 http://localhost:8000")
