from fastapi import APIRouter,Depends,HTTPException
import crud
from schemas import UserResponse,Token
from security import get_db, create_access_token, verify_password
from sqlalchemy.orm import Session
from schemas import UserCreate
from security import hash_password
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()

@router.post("/register",response_model = UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = crud.create_user(db,user.username,hashed_password)
    return new_user


@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token":access_token,"token_type":"bearer"}