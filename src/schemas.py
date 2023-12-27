from datetime import date
from pydantic import BaseModel


class ConnectionCreateSchema(BaseModel):
    operator_code: int
    sub_id: int
    number: str
    tarif_plan: str
    set_date: date
    price: float


class ConnectionSchema(ConnectionCreateSchema):
    id: int

    class Config:
        from_attributes = True


class ConnectionOperatorCreateSchema(BaseModel):
    name: str
    number_count: int


class ConnectionOperatorSchema(ConnectionOperatorCreateSchema):
    code: int
    connections: list[ConnectionSchema]

    class Config:
        from_attributes = True


class SubscriberCreateSchema(BaseModel):
    passport_data: str
    name: str
    surname: str
    address: str


class SubscriberSchema(SubscriberCreateSchema):
    sub_id: int
    connections: list[ConnectionSchema]

    class Config:
        from_attributes = True
