import pytest
from unittest.mock import MagicMock, patch

from app.booking import FlightBooking, save_booking
import app.scraping as search_module


@pytest.fixture
def booking_data():
    return {
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


def test_safe_find_returns_element(booking_data):
    with patch("app.booking.wait_for_element") as mock_wait:
        mock_element = MagicMock()
        mock_wait.return_value = mock_element

        fb = FlightBooking()
        fb.driver = MagicMock()
        element = fb.safe_find("id", "fake")

        assert element == mock_element


def test_safe_find_returns_none_on_timeout(booking_data, caplog):
    with patch("app.booking.wait_for_element", side_effect=Exception("Timeout")):
        fb = FlightBooking()
        fb.driver = MagicMock()
        element = fb.safe_find("id", "missing")
        assert element is None
        assert "Element not found" in caplog.text


def test_search_flow(booking_data):
    fb = FlightBooking()
    fb.driver = MagicMock()

    # Patch helper methods
    fb.open_site = MagicMock(return_value=True)
    fb.select_option = MagicMock(return_value=True)
    fb.click = MagicMock(return_value=True)
    fb.fill_input = MagicMock(return_value=True)
    fb.safe_find = MagicMock()
    fb.safe_find.side_effect = [
        MagicMock(text="Booking Confirmed"),  # confirmation
        MagicMock(text="12345"),              # booking_id
        MagicMock(text="$250.00")             # total_price
    ]

    result = fb.search(booking_data)

    assert result["status"] == "Booking Confirmed"
    assert result["id"] == "12345"
    assert result["price"] == "$250.00"


def test_save_booking_commits_to_db():
    mock_session = MagicMock()
    with patch("app.booking.session", mock_session), \
         patch("app.booking.Booking") as MockBooking:

        result = {"id": "12345", "status": "Confirmed", "price": "250.00"}
        save_booking(result)

        MockBooking.assert_called_once_with(
            booking_id="12345",
            status="Confirmed",
            price=250.00
        )
        assert mock_session.add.called
        assert mock_session.commit.called


@pytest.fixture
def mock_driver():
    """Provide a mocked Selenium driver."""
    driver = MagicMock()
    return driver


@pytest.fixture
def flight_search(mock_driver):
    """Patch Remote driver and return FlightSearch instance."""
    with patch("app.search.webdriver.Remote", return_value=mock_driver):
        fs = search_module.FlightSearch()
        fs.driver = mock_driver
        yield fs


def test_safe_find_success(flight_search):
    with patch("app.search.wait_for_element", return_value="mock_element") as mock_wait:
        el = flight_search.safe_find("id", "myid")
        assert el == "mock_element"
        mock_wait.assert_called_once()


def test_safe_find_timeout(flight_search, caplog):
    with patch("app.search.wait_for_element", side_effect=search_module.TimeoutException):
        el = flight_search.safe_find("id", "missing")
        assert el is None
        assert "Element not found" in caplog.text


def test_select_option_found(flight_search):
    mock_element = MagicMock()
    with patch.object(flight_search, "safe_find", return_value=mock_element):
        with patch("app.search.Select") as mock_select:
            assert flight_search.select_option("fromPort", "Boston")
            mock_select.assert_called_once_with(mock_element)
            mock_select().select_by_visible_text.assert_called_once_with("Boston")


def test_select_option_not_found(flight_search):
    with patch.object(flight_search, "safe_find", return_value=None):
        assert not flight_search.select_option("fromPort", "Boston")


def test_click_found(flight_search):
    mock_element = MagicMock()
    with patch.object(flight_search, "safe_find", return_value=mock_element):
        assert flight_search.click("id", "submit")
        mock_element.click.assert_called_once()


def test_click_not_found(flight_search):
    with patch.object(flight_search, "safe_find", return_value=None):
        assert not flight_search.click("id", "submit")


def test_extract_results(flight_search):
    row1 = MagicMock()
    row1.find_elements.return_value = [MagicMock(text="100"), MagicMock(text="Delta"), MagicMock(text="$200")]

    row2 = MagicMock()
    row2.find_elements.return_value = [MagicMock(text="200"), MagicMock(text="United"), MagicMock(text="$300")]

    flight_search.driver.find_elements.return_value = [MagicMock(), row1, row2]  # skip header

    results = flight_search.extract_results()
    assert results == [
        {"flight": "100", "airline": "Delta", "price": "$200"},
        {"flight": "200", "airline": "United", "price": "$300"},
    ]


def test_save_flights():
    mock_session = MagicMock()
    flights = [
        {"flight": "100", "airline": "Delta", "price": "$200"},
        {"flight": "200", "airline": "United", "price": "$300"},
    ]
    with patch("app.search.session", mock_session), patch("app.search.Flight") as MockFlight:
        search_module.save_flights(flights)
        assert MockFlight.call_count == 2
        mock_session.add.assert_called()
        mock_session.commit.assert_called_once()


def test_search_flights_safe():
    fake_results = [{"flight": "123", "airline": "TestAir", "price": "$100"}]
    with patch.object(search_module, "FlightSearch") as MockSearch, \
         patch.object(search_module, "save_flights") as mock_save:
        instance = MockSearch.return_value.__enter__.return_value
        instance.search.return_value = fake_results

        results = search_module.search_flights_safe("Boston", "London")

        assert results == fake_results
        instance.search.assert_called_once_with("Boston", "London")
        mock_save.assert_called_once_with(fake_results)
