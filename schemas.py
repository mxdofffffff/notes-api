from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True



class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    class Config:
        from_attributes = True

class Meta(BaseModel):
    total: int
    limit: int
    skip: int

class NoteListResponse(BaseModel):
    data: list[NoteResponse]
    meta: Meta


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshRequest(BaseModel):
    refresh_token: str
