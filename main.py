from fastapi import FastAPI
from src import tables
from src.database_setup import engine
from routers.connection_operator import router as connection_operator_router
from routers.subscriber import router as subscriber_router
from routers.connection import router as connection_router


tables.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(router=connection_operator_router, prefix="/connection-operator")
app.include_router(router=subscriber_router, prefix="/subscriber")
app.include_router(router=connection_router, prefix="/connection")