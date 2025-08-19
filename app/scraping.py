from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

from app.decorator import retry
from app.utils import wait_for_element
from app.logger import logger
from app.db import session
from app.models import Flight


class FlightSearch:
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

    def select_option(self, name, text):
        element = self.safe_find(By.NAME, name)
        if element:
            Select(element).select_by_visible_text(text)
            return True
        return False

    def click(self, by, value):
        element = self.safe_find(by, value)
        if element:
            element.click()
            return True
        return False

    def search(self, departure="Boston", destination="London"):
        self.driver.get("https://blazedemo.com")

        # Select cities
        self.select_option("fromPort", departure)
        self.select_option("toPort", destination)

        # Submit search
        self.click(By.CSS_SELECTOR, "input[type='submit']")

        # Extract flight results
        return self.extract_results()

    def extract_results(self):
        flights = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
        results = []
        for flight in flights[1:]:  # skip header
            cols = flight.find_elements(By.TAG_NAME, "td")
            if cols:
                results.append({
                    "flight": cols[0].text,
                    "airline": cols[1].text,
                    "price": cols[-1].text
                })
        return results


def save_flights(flights):
    for f in flights:
        flight = Flight(
            flight_number=f["flight"],
            airline=f["airline"],
            price=float(f["price"].replace('$',''))
        )
        session.add(flight)
    session.commit()


@retry(times=3)
def search_flights_safe(departure="Boston", destination="London"):
    with FlightSearch() as search:
        search_results = search.search(departure, destination)
        save_flights(search_results)
        return search_results


if __name__ == "__main__":
    flights = search_flights_safe()
    for f in flights:
        print(f)
