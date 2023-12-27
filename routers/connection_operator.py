from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas import ConnectionOperatorSchema, ConnectionOperatorCreateSchema
from src.tables import ConnectionOperator
from src.database_setup import get_db

from . import CHUNK_SIZE


router = APIRouter()


@router.get("/", response_model=list[ConnectionOperatorSchema])
def read(p: int = 0, db: Session = Depends(get_db)):
    skip = p * CHUNK_SIZE
    limit = CHUNK_SIZE
    return db.query(ConnectionOperator).order_by(ConnectionOperator.code).offset(skip).limit(limit).all()


@router.post("/", response_model=ConnectionOperatorSchema)
def create(data: ConnectionOperatorCreateSchema, db: Session = Depends(get_db)):
    co = ConnectionOperator(**data.dict())
    db.add(co)
    db.commit()
    return co


def from_id(db: Session, id: int):
    return db.query(ConnectionOperator).filter(ConnectionOperator.code == id)


@router.put("/{id}")
def update(id: int, data: ConnectionOperatorCreateSchema, db: Session = Depends(get_db)):
    co = from_id(db, id).first()
    co.number_count = data.number_count
    db.commit()
    return db


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    co = from_id(db, id).delete()
    db.commit()
    return co