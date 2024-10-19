from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.controllers.auth_controller import auth_router
from src.controllers.item_controller import item_router
from src.controllers.user_controller import user_router

load_dotenv()


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(prefix="/api", router=item_router)
app.include_router(prefix="/api", router=auth_router)

app.include_router(prefix="/api", router=user_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
