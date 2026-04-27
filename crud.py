from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User,Note
from schemas import NoteUpdate


def get_user_by_username(db:Session, username: str):
    db_user = db.query(User).filter(User.username == username).first()
    return db_user

def create_user(db:Session, username: str, hashed_password: str):
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_note(db:Session, title: str, content: str,user_id:int):
    new_note = Note(title=title, content=content, user_id=user_id , is_favorite = False)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def edit_note(db:Session, note_id:int, note_data:NoteUpdate,user_id:int):
    db_note = db.query(Note).filter(Note.id == note_id,Note.user_id == user_id,Note.is_deleted == False).first()
    if db_note is None:
        return None
    if note_data.title is not None:
        db_note.title = note_data.title
    if note_data.content is not None:
        db_note.content = note_data.content
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes_by_user(
        db:Session,
        user_id:int,
        limit:int = 10,
        skip:int = 0,
        search:str = None,
        sort:str = None,
        date_from = None,
        date_to = None
):
    query=db.query(Note).filter(Note.user_id == user_id,Note.is_deleted == False)
    if search:
        query = query.filter(Note.title.ilike(f"%{search}%"))
    if date_from:
        query = query.filter(Note.created_at >= date_from)
    if date_to:
        query = query.filter(Note.created_at <= date_to)
    if sort == "asc":
        query = query.order_by(Note.id.asc())
    elif sort == "desc":
        query = query.order_by(Note.id.desc())
    total = query.count()
    items = query.limit(limit).offset(skip).all()
    return items,total


def get_note(db:Session, note_id:int,user_id:int):
    db_note = db.query(Note).filter(Note.id == note_id,Note.user_id == user_id,Note.is_deleted == False).first()
    if db_note is None:
        return None
    return db_note

def delete_note(db:Session,note_id:int,user_id:int):
    note = db.query(Note).filter(Note.id == note_id,Note.user_id==user_id,Note.is_deleted == False).first()
    if note is None:
        return None
    note.is_deleted = True
    db.commit()
    return note


def restore_note(db:Session,note_id:int,user_id:int):
    note = db.query(Note).filter(Note.id == note_id,Note.user_id==user_id,Note.is_deleted == True).first()
    if note is None:
        return None
    note.is_deleted = False
    db.commit()
    return note


def get_deleted_notes(db:Session,user_id:int):
    note = db.query(Note).filter(Note.user_id == user_id,Note.is_deleted == True).all()
    if note is None:
        return None
    return note

def get_favorites(db:Session,user_id:int):
    notes = db.query(Note).filter(Note.user_id == user_id,Note.is_favorite == True).all()
    if notes is None:
        return None
    return notes

def like_note(db:Session,note_id:int,user_id:int):
    note = db.query(Note).filter(Note.id == note_id,Note.user_id == user_id,Note.is_deleted == False).first()
    if note is None:
        return None
    note.is_favorite = True
    db.commit()
    db.refresh(note)
    return note
