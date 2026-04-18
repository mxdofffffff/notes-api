import crud
from fastapi import HTTPException


def create_note(db,note_data,current_user):
    return crud.create_note(db,note_data.title,note_data.content,current_user.id)

def get_notes(db,current_user,limit,skip,search = None):
    return crud.get_notes_by_user(db,current_user.id,limit,skip,search)

def update_note(db,note_id,note_data,current_user):
    note = crud.get_note(db, note_id, current_user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud.edit_note(db, note_id, note_data.title, note_data.content)

def delete_note(db,note_id,current_user):
    note = crud.get_note(db, note_id, current_user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud.delete_note(db, note_id)