from fastapi import FastAPI
from src.routers.item import item_router

app = FastAPI()
app.include_router(item_router)
