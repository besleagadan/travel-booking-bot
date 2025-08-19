
import time
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import OperationalError

from app.db import Base, engine


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    flight_number = Column(String)
    airline = Column(String)
    price = Column(Float)

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    booking_id = Column(String)
    status = Column(String)
    price = Column(Float)



def init_db():
    for _ in range(10):
        try:
            Base.metadata.create_all(engine)
            break
        except OperationalError:
            print("Postgres not ready, retrying...")
            time.sleep(2)

