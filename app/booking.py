from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

from app.db import session
from app.models import Booking
from app.logger import logger
from app.utils import wait_for_element


class FlightBooking:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=options
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def safe_find(self, by, value, timeout=10):
        try:
            return wait_for_element(self.driver, by, value, timeout)
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            return None

    def select_option(self, name, option_text):
        element = self.safe_find(By.NAME, name)
        if element:
            Select(element).select_by_visible_text(option_text)
            return True
        return False

    def click(self, by, value):
        element = self.safe_find(by, value)
        if element:
            element.click()
            return True
        return False

    def fill_input(self, field_id, text):
        element = self.safe_find(By.ID, field_id)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False

    def open_site(self, url="https://blazedemo.com"):
        self.driver.get(url)
        if "captcha" in self.driver.page_source.lower():
            logger.error("CAPTCHA detected, skipping...")
            return False
        return True

    def search(self, data):
        self.open_site("https://blazedemo.com")

        self.select_option("fromPort", data["from"])
        self.select_option("toPort", data["to"])
        self.click(By.CSS_SELECTOR, "input[type='submit']")

        self.click(By.CSS_SELECTOR, "table tr:nth-child(2) input")

        for field, value in data["passenger"].items():
            self.fill_input(field, value)

        self.click(By.CSS_SELECTOR, "input[type='submit']")

        confirmation = self.safe_find(By.TAG_NAME, "h1").text
        booking_id = self.safe_find(By.CSS_SELECTOR, "table tr:nth-child(1) td:nth-child(2)").text
        total_price = self.safe_find(By.CSS_SELECTOR, "table tr:nth-child(3) td:nth-child(2)").text

        return {"status": confirmation, "id": booking_id, "price": total_price}


def save_booking(result):
    if result:
        booking = Booking(
            booking_id=result["id"],
            status=result["status"],
            price=float(result["price"].replace('USD', ''))
        )
        session.add(booking)
        session.commit()


if __name__ == "__main__":
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

    flight = FlightBooking()
    result = flight.book(booking_data)
    save_booking(result)
    print(result)
