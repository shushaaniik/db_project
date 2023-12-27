from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import declarative_base, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()



class Connection(Base):
    __tablename__ = "connection"
    
    id = Column(Integer, primary_key=True, index = True)
    operator_code = mapped_column(ForeignKey("connection_operator.code", ondelete="CASCADE"))
    sub_id = mapped_column(ForeignKey("subscriber.sub_id", ondelete="CASCADE"))
    number = Column(String, default="")
    tarif_plan = Column(String, default="")
    set_date = Column(Date)
    price = Column(Numeric(10, 2))

    operator = relationship("ConnectionOperator", back_populates="connections")
    subscriber = relationship("Subscriber", back_populates="connections")



class ConnectionOperator(Base):
    __tablename__ = "connection_operator"

    code = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    number_count = Column(Integer, default=0)

    connections = relationship(Connection, back_populates="operator")



class Subscriber(Base):
    __tablename__ = "subscriber"

    sub_id = Column(Integer, primary_key=True, index=True)
    passport_data = Column(String, index=True)
    name = Column(String)
    surname = Column(String)
    sursurname = Column(String)
    address = Column(String)

    connections = relationship(Connection, back_populates="subscriber")
