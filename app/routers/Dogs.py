from fastapi import APIRouter, HTTPException , status
from app.models.Dogs import Dogs
from sqlmodel import Session, select

router = APIRouter(prefix="/Dogs", tags=["Dogs"])
from ..database import engine

@router.get("/", summary="Get all Dogs")
async def get_all():
    with Session(engine) as session:
        statement = select(Dogs)
        results = session.exec(statement).all()
        return results



@router.post("/", summary="Create a new Dogs", status_code=status.HTTP_201_CREATED)
async def create_item(_Dogs : Dogs):
    with Session(engine) as session:
        session.add(_Dogs)
        session.commit()
        session.refresh(_Dogs)
        return _Dogs


@router.get("/{item_id}", summary="Get Dogs by ID")
async def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Dogs, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dogs not found")
        return item



@router.put("/{item_id}", summary="Update Dogs")
async def update_item(_Dogs : Dogs , item_id: int):
    with Session(engine) as session:

        item = session.get(Dogs, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dogs not found")

        for key, value in _Dogs.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@router.delete("/{item_id}", summary="Delete Dogs" ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):

    with Session(engine) as session:
        item = session.get(Dogs, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dogs not found")

        session.delete(item)
        session.commit()
        return None
