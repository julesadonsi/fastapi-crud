from typing import Any, Sequence, Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Row, RowMapping, select
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.item import Item
from src.schemas.item import Item as ItemSchema, ItemCreate, ItemUpdate

item_router = APIRouter()


@item_router.get("/items")
async def get_items(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
) -> Sequence[ItemSchema]:
    stmt = select(Item).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@item_router.post("/items")
async def create_item(data: ItemCreate, db: Session = Depends(get_db)) -> ItemSchema:
    item = Item(**data.model_dump())
    db.add(item)
    await db.commit()
    return item


@item_router.put("/items/{item_id}")
async def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    try:
        item = await db.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, val in data.model_dump(exclude_none=True).items():
            setattr(item, key, val)
            await db.commit()
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@item_router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    item = db.get(Item, item_id)
    await db.delete(item)
    await db.commit()
    return {"message": "Item successfully deleted"}
