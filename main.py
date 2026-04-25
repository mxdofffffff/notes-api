from fastapi.responses import JSONResponse
from fastapi import FastAPI,Request
from database import engine,Base
from routers import notes, auth
from fastapi.exceptions import HTTPException

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request,exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error":{
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )

app.include_router(notes.router)
app.include_router(auth.router)