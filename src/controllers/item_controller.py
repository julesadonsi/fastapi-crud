from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session

from src.db import get_db
from src.models.user_model import Item
from src.schemas.item_schema import ItemCreate, ItemSchema, ItemUpdate
from src.services.auth_service import authenticated

item_router = APIRouter()


@item_router.get("/items", response_model=List[ItemSchema])
async def get_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    statement = select(Item).options(selectinload(Item.user)).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()


@item_router.post("/items", response_model=ItemSchema)
async def create_item(
    data: ItemCreate, db: AsyncSession = Depends(get_db), user=Depends(authenticated)
):
    item = Item(**data.model_dump(), user=user)
    db.add(item)
    await db.commit()
    return item


@item_router.put("/items/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    user: Session = Depends(authenticated),
):
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
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):

    try:
        item = await db.get(Item, item_id)
        await db.delete(item)
        await db.commit()
        return {"message": "Item deleted", "status": 200}

    except Exception as exception:
        raise HTTPException(status_code=404, detail="Item not found")
