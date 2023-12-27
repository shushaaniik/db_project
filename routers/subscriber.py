from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas import SubscriberSchema, SubscriberCreateSchema
from src.tables import Subscriber
from src.database_setup import get_db

from . import CHUNK_SIZE


router = APIRouter()


@router.get("/", response_model=list[SubscriberSchema])
def read(p: int = 0, db: Session = Depends(get_db)):
    skip = p * CHUNK_SIZE
    limit = CHUNK_SIZE
    return db.query(Subscriber).order_by(Subscriber.sub_id).offset(skip).limit(limit).all()


@router.post("/", response_model=SubscriberSchema)
def create(data: SubscriberCreateSchema, db: Session = Depends(get_db)):
    s = Subscriber(**data.dict())
    db.add(s)
    db.commit()
    return s


def from_id(db: Session, id: int):
    return db.query(Subscriber).filter(Subscriber.sub_id == id)


@router.put("/{id}")
def update(id: int, data: SubscriberCreateSchema, db: Session = Depends(get_db)):
    s = from_id(db, id).first()
    s.address = data.address
    db.commit()
    return db


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    s = from_id(db, id).delete()
    db.commit()
    return s