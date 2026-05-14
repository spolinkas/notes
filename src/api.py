from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import get_connection

class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class CreateNote(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str

router = APIRouter()

@router.get("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return notes


@router.post("/notes")
def create_note(note: CreateNote):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s) returning *', (note.title, note.content))
    note = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return note

@router.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE notes
        SET title = %s, content = %s
        WHERE id = %s
        RETURNING *;
        """,
        (note.title, note.content, note_id)
    )

    updated_note = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return updated_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM notes WHERE id = %s RETURNING *;",
        (note_id,)
    )

    deleted_note = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "message": "Note deleted",
        "note": deleted_note
    }

@router.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes WHERE id = %s;", (note_id,))
    note = cur.fetchone()

    cur.close()
    conn.close()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note
