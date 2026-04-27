from fastapi import APIRouter,Depends,HTTPException,Query
import crud
from schemas import NoteResponse, NoteUpdate,NoteCreate,NoteListResponse
from security import get_db
from sqlalchemy.orm import Session
from security import get_current_user
from services import note_service
from datetime import datetime
router = APIRouter()

@router.post("/notes",response_model=NoteResponse)
def create_note(note:NoteCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.create_note(db,note,current_user)


@router.get("/notes",response_model=NoteListResponse)
def get_notes(
        db:Session = Depends(get_db),
        current_user = Depends(get_current_user),
        limit:int =Query(default=10,le=100,ge=1),
        skip:int = Query(default=0,ge=0),
        search:str = Query(default=None),
        sort:str = Query(default=None),
        date_from:datetime = Query(default=None),
        date_to:datetime = Query(default=None)
):
    return note_service.get_notes(db,current_user,limit,skip,search,sort,date_from,date_to)


@router.patch("/notes/{note_id}",response_model=NoteResponse)
def edit_notes(note_id:int,note_data:NoteUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.update_note(db,note_id,note_data,current_user)


@router.delete("/notes/{note_id}")
def delete_note(note_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.delete_note(db,note_id,current_user)

@router.post("/notes/{note_id}/restore",response_model=NoteResponse)
def restore_note(note_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.restore_note(db,note_id,current_user)

@router.get("/notes/deleted",response_model=list[NoteResponse])
def get_deleted_notes(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.get_deleted_notes(db,current_user)


@router.get("/notes/favorites",response_model=list[NoteResponse])
def get_favorites(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.get_favorites(db,current_user)


@router.post("/notes/{note_id}/favorite",response_model=NoteResponse)
def like_note(note_id: int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return note_service.like_note(db,note_id,current_user)