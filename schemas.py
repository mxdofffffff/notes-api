from pydantic import BaseModel,Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3,max_length=30)
    password: str = Field(min_length=4,max_length=30)


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True



class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    is_favorite: bool | None
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
    title: str | None = Field(default=None,min_length=1,max_length=100)
    content: str | None = Field(default=None,min_length=1,max_length=1000)
    is_favorite: bool | None = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshRequest(BaseModel):
    refresh_token: str
