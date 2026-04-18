from fastapi import APIRouter,Depends,HTTPException,Query
import crud
from schemas import NoteResponse, NoteUpdate,NoteCreate
from security import get_db
from sqlalchemy.orm import Session
from security import get_current_user
from services import note_service
router = APIRouter()

@router.post("/notes",response_model=NoteResponse)
def create_note(note:NoteCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.create_note(db,note,current_user)


@router.get("/notes",response_model=list[NoteResponse])
def get_notes(db:Session = Depends(get_db),current_user = Depends(get_current_user),limit:int =Query(default=10,le=100,ge=1),skip:int = Query(default=0,ge=0),search:str = Query(default=None)):
    return note_service.get_notes(db,current_user,limit,skip,search)


@router.patch("/notes/{note_id}",response_model=NoteResponse)
def edit_notes(note_id:int,note_data:NoteUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.update_note(db,note_id,note_data,current_user)


@router.delete("/notes/{note_id}")
def delete_note(note_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    note_service.delete_note(db,note_id,current_user)
    return {"message":"Note deleted successfully"}