from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

Base = declarative_base()

# Connect to PostgreSQL
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
