import crud
from fastapi import HTTPException


def create_note(db,note_data,current_user):
    return crud.create_note(db,note_data.title,note_data.content,current_user.id)

def get_notes(db,current_user,limit,skip,search = None,sort = None,date_from = None,date_to = None):
    items,total= crud.get_notes_by_user(db,current_user.id,limit,skip,search,sort,date_from,date_to)
    return {
        "items":items,
        "total":total,
        "limit":limit,
        "skip":skip,
    }

def update_note(db,note_id,note_data,current_user):
    note = crud.edit_note(db, note_id,note_data, current_user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def delete_note(db,note_id,current_user):
    note = crud.delete_note(db, note_id, current_user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message":"Note deleted successfully"}


def restore_note(db,note_id,current_user):
    note = crud.restore_note(db, note_id, current_user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def get_deleted_notes(db,current_user):
    notes = crud.get_deleted_notes(db, current_user.id)
    if notes is None:
        raise HTTPException(status_code=404, detail="Notes not found")
    return notes