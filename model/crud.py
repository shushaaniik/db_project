from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from core import SessionLocal, ConnectionOperator, Subscriber, Connection
from pydantic import BaseModel

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations for Connection Operators
@app.post("/operators/", response_model=ConnectionOperator)
def create_operator(operator: ConnectionOperator, db: Session = Depends(get_db)):
    db_operator = ConnectionOperator(**operator.dict())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


@app.get("/operators/{operator_code}", response_model=ConnectionOperator)
def read_operator(operator_code: int, db: Session = Depends(get_db)):
    db_operator = db.query(ConnectionOperator).filter(ConnectionOperator.code == operator_code).first()
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator


@app.get("/operators/", response_model=List[ConnectionOperator])
def read_all_operators(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    operators = db.query(ConnectionOperator).offset(skip).limit(limit).all()
    return operators


@app.put("/operators/{operator_code}", response_model=ConnectionOperator)
def update_operator(operator_code: int, name: str, number_count: int, db: Session = Depends(get_db)):
    db_operator = db.query(ConnectionOperator).filter(ConnectionOperator.code == operator_code).first()
    if db_operator:
        db_operator.name = name
        db_operator.number_count = number_count
        db.commit()
        db.refresh(db_operator)
        return db_operator
    raise HTTPException(status_code=404, detail="Operator not found")


@app.delete("/operators/{operator_code}", response_model=ConnectionOperator)
def delete_operator(operator_code: int, db: Session = Depends(get_db)):
    db_operator = db.query(ConnectionOperator).filter(ConnectionOperator.code == operator_code).first()
    if db_operator:
        db.delete(db_operator)
        db.commit()
        return db_operator
    raise HTTPException(status_code=404, detail="Operator not found")


# CRUD operations for Subscribers
@app.post("/subscribers/", response_model=Subscriber)
def create_subscriber(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    db_subscriber = Subscriber(**subscriber.dict())
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


@app.get("/subscribers/{passport_data}", response_model=Subscriber)
def read_subscriber(passport_data: str, db: Session = Depends(get_db)):
    db_subscriber = db.query(Subscriber).filter(Subscriber.passport_data == passport_data).first()
    if db_subscriber:
        return db_subscriber
    raise HTTPException(status_code=404, detail="Subscriber not found")


@app.get("/subscribers/", response_model=List[Subscriber])
def read_all_subscribers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).offset(skip).limit(limit).all()
    return subscribers


@app.put("/subscribers/{passport_data}", response_model=Subscriber)
def update_subscriber(passport_data: str, name: str, surname: str, address: str = "",
                      db: Session = Depends(get_db)):
    db_subscriber = db.query(Subscriber).filter(Subscriber.passport_data == passport_data).first()
    if db_subscriber:
        db_subscriber.name = name
        db_subscriber.surname = surname
        db_subscriber.address = address
        db.commit()
        db.refresh(db_subscriber)
        return db_subscriber
    raise HTTPException(status_code=404, detail="Subscriber not found")


@app.delete("/subscribers/{passport_data}", response_model=Subscriber)
def delete_subscriber(passport_data: str, db: Session = Depends(get_db)):
    db_subscriber = db.query(Subscriber).filter(Subscriber.passport_data == passport_data).first()
    if db_subscriber:
        db.delete(db_subscriber)
        db.commit()
        return db_subscriber
    raise HTTPException(status_code=404, detail="Subscriber not found")


# CRUD operations for Connections
@app.post("/connections/", response_model=Connection)
def create_connection(connection: ConnectionCreate, db: Session = Depends(get_db)):
    db_connection = Connection(**connection.dict())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@app.get("/connections/{operator_code}/{passport_data}", response_model=Connection)
def read_connection(operator_code: int, passport_data: str, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(
        Connection.operator_code == operator_code,
        Connection.passport_data == passport_data
    ).first()
    if db_connection:
        return db_connection
    raise HTTPException(status_code=404, detail="Connection not found")


@app.get("/connections/", response_model=List[Connection])
def read_all_connections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    connections = db.query(Connection).offset(skip).limit(limit).all()
    return connections


@app.put("/connections/{operator_code}/{passport_data}", response_model=Connection)
def update_connection(operator_code: int, passport_data: str, number: str, tarif_plan: str,
                      set_date: str, price: float, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(
        Connection.operator_code == operator_code,
        Connection.passport_data == passport_data
    ).first()
    if db_connection:
        db_connection.number = number
        db_connection.tarif_plan = tarif_plan
        db_connection.set_date = set_date
        db_connection.price = price
        db.commit()
        db.refresh(db_connection)
        return db_connection
    raise HTTPException(status_code=404, detail="Connection not found")


@app.delete("/connections/{operator_code}/{passport_data}", response_model=Connection)
def delete_connection(operator_code: int, passport_data: str, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(
        Connection.operator_code == operator_code,
        Connection.passport_data == passport_data
    ).first()
    if db_connection:
        db.delete(db_connection)
        db.commit()
        return db_connection
    raise HTTPException(status_code=404, detail="Connection not found")
