from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.sql import func
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

Base = declarative_base()


class ConnectionOperator(Base):
    __tablename__ = "connection_operator"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    number_count = Column(Integer, default=0)

    connections = relationship("Connection", back_populates="operator")


class Subscriber(Base):
    __tablename__ = "subscriber"

    passport_data = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    address = Column(String, default="")

    connections = relationship("Connection", back_populates="subscriber")


class Connection(Base):
    __tablename__ = "connection"

    operator_code = Column(Integer, ForeignKey("connection_operator.code"), nullable=False)
    passport_data = Column(String, ForeignKey("subscriber.passport_data"), nullable=False)
    number = Column(String, default="")
    tarif_plan = Column(String, default="")
    set_date = Column(Date)
    price = Column(Numeric(10, 2))

    operator = relationship("ConnectionOperator", back_populates="connections")
    subscriber = relationship("Subscriber", back_populates="connections")
