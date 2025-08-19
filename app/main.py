from app.logger import logger

from app.models import init_db
from app.scraping import FlightSearch, save_flights
from app.booking import FlightBooking, save_booking


def main():
    # Initialize database
    init_db()
    logger.info("Database initialized.")

    # Search flights
    flightsearch = FlightSearch()
    search_results = flightsearch.search(departure="Boston", destination="London")
    logger.info(f"Found {len(search_results)} flights.")

    # Save flight results to database
    save_flights(search_results)
    logger.info("Flight results saved to database.")

    # Book a flight (first result)
    booking_data = {
        "from": "Boston",
        "to": "London",
        "passenger": {
            "inputName": "Dan Coder",
            "address": "123 Python Street",
            "city": "Chisinau",
            "state": "MD",
            "zipCode": "2001",
            "creditCardNumber": "4111111111111111",
            "nameOnCard": "Dan Coder"
        }
    }

    flightbooking = FlightBooking()
    booking_result = flightbooking.search(booking_data)
    logger.info("Booking completed:", booking_result)

    # Save booking to database
    save_booking(booking_result)
    logger.info("Booking saved to database.")


if __name__ == "__main__":
    main()
