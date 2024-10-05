from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import Item
from src.schemas.item_schema import ItemCreate, ItemUpdate, ItemSchema
from src.services.auth_service import authenticated

item_router = APIRouter()


@item_router.get("/items")
async def get_items(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
) -> Sequence[ItemSchema]:
    result = db.query(Item).offset(skip).limit(limit).all()
    return result


@item_router.post("/items", response_model=ItemSchema)
async def create_item(
    data: ItemCreate, db: Session = Depends(get_db), user=Depends(authenticated)
):
    item = Item(**data.model_dump(), user=user)
    db.add(item)
    db.commit()
    return item


@item_router.put("/items/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    user: Session = Depends(authenticated),
):
    try:
        item = db.query(Item).filter_by(id=item_id).one()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, val in data.model_dump(exclude_none=True).items():
            setattr(item, key, val)
            db.commit()
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@item_router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    item = db.get(Item, item_id)
    db.delete(item)
    db.commit()
    return {"message": "Item successfully deleted"}
