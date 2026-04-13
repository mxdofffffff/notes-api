from fastapi import FastAPI
from database import engine,Base
from routers import notes, auth

app = FastAPI()

Base.metadata.create_all(engine)


app.include_router(notes.router)
app.include_router(auth.router)