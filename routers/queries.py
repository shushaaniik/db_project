from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.schemas import SubscriberSchema, ConnectionOperatorSchema, ConnectionSchema
from src.tables import Subscriber, ConnectionOperator, Connection
from src.database_setup import get_db

from . import CHUNK_SIZE


router = APIRouter()


@router.get("/select", response_model=list[ConnectionOperatorSchema])
def select(p: int = 0, key: str = "code", db: Session = Depends(get_db)):
    skip = p * CHUNK_SIZE
    limit = CHUNK_SIZE
    query = (
        db.query(ConnectionOperator)
        .where(ConnectionOperator.name == "Mcdonald PLC")
        .where(ConnectionOperator.number_count > 50) 
    )
    match key:
        case "code":
            query = query.order_by(ConnectionOperator.code)
        case "name":
            query = query.order_by(ConnectionOperator.name)
        case "number_count":
            query = query.order_by(ConnectionOperator.number_count)
    return query.offset(skip).limit(limit).all()

@router.get("/join", response_model=list[tuple[ConnectionOperatorSchema, SubscriberSchema]])
def join(p: int = 0, key: str = "code", db: Session = Depends(get_db)):
    skip = p * CHUNK_SIZE
    limit = CHUNK_SIZE
    query = (
        db.query(Connection, ConnectionOperator, Subscriber)
        .join(ConnectionOperator, ConnectionOperator.code == Connection.operator_code)
        .join(Subscriber, Subscriber.sub_id == Connection.sub_id)
    )
    match key:
        case "sub_id":
            query = query.order_by(Subscriber.id)
        case "code":
            query = query.order_by(ConnectionOperator.code)
    query = query.offset(skip).limit(limit).all()
    return [(op, sub) for _, op, sub in query]


@router.get("/group_by", response_model=list[dict[str, float]])
def group_by(p: int = 0, db: Session = Depends(get_db)):
    skip = p * CHUNK_SIZE
    limit = CHUNK_SIZE
    query = (
        db.query(ConnectionOperator.number_count, func.avg(Subscriber.sub_id))
        .group_by(ConnectionOperator.number_count)
        .order_by(ConnectionOperator.number_count)
    )
    return [{"number_count": number_count, "average": average}
            for (number_count, average) in query.offset(skip).limit(limit).all()]


@router.put("/update")
def update(db: Session = Depends(get_db)):
    db.query(Connection).filter(Connection.price < 1000).update({"price": Connection.price * 2})
    db.commit()
    return db
