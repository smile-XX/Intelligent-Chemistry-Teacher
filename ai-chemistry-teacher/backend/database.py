"""
数据库模块 - SQLite 错题本
"""
import sqlite3
import os

DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, "data.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wrong_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            tags TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_wrong_question(question: str, answer: str, tags: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wrong_questions (question, answer, tags) VALUES (?, ?, ?)",
                   (question, answer, tags))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def list_wrong_questions():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT id, question, tags, created_at FROM wrong_questions ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_wrong_question(question_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM wrong_questions WHERE id = ?", (question_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_wrong_question(question_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wrong_questions WHERE id = ?", (question_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
