from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.db import init_db
from src.controllers.auth_controller import auth_router
from src.controllers.item_controller import item_router

app = FastAPI()

load_dotenv()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"detail": exc.errors(), "body": exc.body}
    )


app.include_router(item_router)
app.include_router(auth_router)
