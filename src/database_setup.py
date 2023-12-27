from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


url = URL.create(drivername="postgresql",
                 username="admin",
                 password="secret",
                 host="localhost",
                 database="connection_operators",
                 port=5432)

engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
