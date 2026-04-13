from fastapi import APIRouter,Depends,HTTPException,Query
import crud
from schemas import NoteResponse, NoteUpdate,NoteCreate
from security import get_db
from sqlalchemy.orm import Session
from security import get_current_user
router = APIRouter()

@router.post("/notes",response_model=NoteResponse)
def create_note(note:NoteCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return crud.create_note(db,note.title,note.content,current_user.id)


@router.get("/notes",response_model=list[NoteResponse])
def get_notes(db:Session = Depends(get_db),current_user = Depends(get_current_user),limit:int =Query(default=10,le=100,ge=1),skip:int = Query(default=0,ge=0)):
    notes = crud.get_notes_by_user(db,current_user.id,limit,skip)
    return notes


@router.patch("/notes/{note_id}",response_model=NoteResponse)
def edit_notes(note_id:int,note_data:NoteUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    note = crud.get_note(db,note_id,current_user.id)
    if note is None:
        raise HTTPException(status_code=404,detail="Note not found")
    update_note=crud.edit_note(db,note_id,note_data.title,note_data.content,current_user.id)
    return update_note


@router.delete("/notes/{note_id}")
def delete_note(note_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    note = crud.get_note(db,note_id,current_user.id)
    if note is None:
        raise HTTPException(status_code=404,detail="Note not found")
    crud.delete_note(db,note.id,current_user.id)
    return {"message":"Note deleted successfully"}