from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas import ConnectionSchema, ConnectionCreateSchema
from src.tables import Connection
from src.database_setup import get_db


router = APIRouter()


@router.get("/", response_model=list[ConnectionSchema])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Connection).order_by(Connection.id).offset(skip).limit(limit).all()


@router.post("/", response_model=ConnectionSchema)
def create(data: ConnectionCreateSchema, db: Session = Depends(get_db)):
    c = Connection(**data.dict())
    db.add(c)
    db.commit()
    return c


def from_id(db: Session, id: int):
    return db.query(Connection).filter(Connection.id == id)


@router.put("/{id}")
def update(id: int, data: ConnectionCreateSchema, db: Session = Depends(get_db)):
    c = from_id(db, id).first()
    c.number = data.number
    c.tarif_plan = data.tarif_plan
    c.price = data.price
    db.commit()
    return db


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    c = from_id(db, id).delete()
    db.commit()
    return c