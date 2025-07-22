from databases import Database
from sqlalchemy import create_engine
from backend.core.models import metadata  

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


metadata.create_all(bind=engine)
