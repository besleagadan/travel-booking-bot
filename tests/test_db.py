import pytest
from app.db import Base, Flight, Booking, engine, Session

@pytest.fixture(scope="module")
def session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_insert_flight(session):
    flight = Flight(flight_number="UA123", airline="United Airlines", price=400)
    session.add(flight)
    session.commit()

    result = session.query(Flight).filter_by(flight_number="UA123").first()
    assert result.airline == "United Airlines"
    assert result.price == 400

def test_insert_booking(session):
    booking = Booking(booking_id="B123", status="Confirmed", price=500)
    session.add(booking)
    session.commit()

    result = session.query(Booking).filter_by(booking_id="B123").first()
    assert result.status == "Confirmed"
    assert result.price == 500
