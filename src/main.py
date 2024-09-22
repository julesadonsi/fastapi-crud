from fastapi import FastAPI

from src.db import init_db
from src.routers.item import item_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(item_router)
