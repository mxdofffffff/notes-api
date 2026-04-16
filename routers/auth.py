from fastapi import APIRouter,Depends,HTTPException
from jose import jwt,JWTError
import crud
from schemas import UserResponse,Token
from security import get_db, create_access_token, verify_password, create_refresh_token, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from schemas import UserCreate,RefreshRequest
from security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from models import RefreshToken


router = APIRouter()

@router.post("/register",response_model = UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = crud.create_user(db,user.username,hashed_password)
    return new_user


@router.post("/refresh")
def refresh(data:RefreshRequest,db:Session = Depends(get_db)):
    db_token=db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()
    if not db_token:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    try:
        payload = jwt.decode(data.refresh_token,SECRET_KEY,algorithms = [ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Incorrect username or password")
    except JWTError:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    new_user = crud.get_user_by_username(db, username=username)
    if not new_user:
        raise HTTPException(status_code=401,detail="User does not exist")
    new_access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token":new_access_token,"token_type":"bearer"}



@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    db_token = RefreshToken(token = refresh_token,user_id=db_user.id)
    db.add(db_token)
    db.commit()
    return {"access_token":access_token,"refresh_token":refresh_token ,"token_type":"bearer"}


@router.post("/logout")
def logout(data:RefreshRequest,db:Session = Depends(get_db)):
    db_token=db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()
    if not db_token:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    db.delete(db_token)
    db.commit()
    return {"message":"You have been logged out"}