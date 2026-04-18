from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User,Note

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
    new_note = Note(title=title, content=content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def edit_note(db:Session, note_id:int, title: str, content: str):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        return None
    db_note.title = title
    db_note.content = content
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes_by_user(db:Session, user_id:int,limit:int = 10, skip:int = 0,search:str = None):
    query=db.query(Note).filter(Note.user_id == user_id)
    if search:
        query = query.filter(Note.title.contains(search))
    query = query.offset(skip).limit(limit)
    return query.all()

def get_note(db:Session, note_id:int,user_id:int):
    db_note = db.query(Note).filter(Note.id == note_id,Note.user_id== user_id).first()
    if db_note is None:
        return None
    return db_note

def delete_note(db:Session,note_id:int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        return None
    db.delete(note)
    db.commit()
    return note
