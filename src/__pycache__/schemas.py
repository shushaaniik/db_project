from datetime import date
from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    operator_code: int
    sub_id: int
    number: str
    tarif_plan: str
    set_date: date
    price: int


class Connection(ConnectionCreate):
    id: int

    class Config:
        from_attributes = True


class ConnectionOperatorCreate(BaseModel):
    name: str
    number_count: int


class ConnectionOperator(ConnectionOperatorCreate):
    code: int
    connections: list[Connection]

    class Config:
        from_attributes = True


class SubscriberCreate(BaseModel):
    passport_data: str
    name: str
    surname: str
    address: str


class Subscriber(SubscriberCreate):
    sub_id: int
    connections: list[Connection]

    class Config:
        from_attributes = True
