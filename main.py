from fastapi.responses import JSONResponse
from fastapi import FastAPI,Request
from database import engine,Base
from routers import notes, auth
from fastapi.exceptions import HTTPException
import time
from fastapi import Request
import asyncio

app = FastAPI()
Base.metadata.create_all(bind = engine)
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

@app.middleware("http")
async def log_requests(request: Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print (
        f"{request.method} {request.url.path} "
        f"{response.status_code} "
        f"Took {process_time:.4f} seconds"
    )
    return response

@app.get("/async-test")
async def async_test():
    await asyncio.sleep(5)
    return {"message":"ok"}

@app.get("/sync-test")
async def sync_test():
    time.sleep(5)
    return {"message":"okay"}

app.include_router(notes.router)
app.include_router(auth.router)