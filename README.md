# Travel Booking Automation Bot

An automation bot that simulates booking flights using Selenium.
It searches flights, fills booking forms, and saves ticket details into PostgreSQL.
The project is containerized with Docker and tested with pytest.

## Tech Stack
- Python 3.11
- Uv
- Selenium
- PostgreSQL
- SQLAlchemy
- Docker + Docker Compose
- Pytest
- GitHub Actions (CI)

---

## Project Roadmap

### Phase 1 — Setup
Created the foundation of the project with a clean and professional structure.
Initialized Git, virtual environment, and dependencies.
Added `README.md`, `.gitignore`, and base folders (`app/`, `tests/`).
This step ensures the project is easy to navigate and ready for development.

### Phase 2 — Basic Selenium Workflow
Built the first automation flow with Selenium.
The bot navigates to a demo travel site, searches flights, and extracts flight details (airline, flight ID, price).
This step proves the core automation works and sets the stage for booking simulation.

### Phase 3 — Booking Simulation
Extended the workflow to book a flight automatically.
The bot selects a flight, fills a booking form with test data, and extracts a confirmation receipt (ID and price).
This step demonstrates a complete user journey from search to booking.

### Phase 4 — Error Handling
Improved bot reliability with robust error handling.
Added explicit waits for dynamic content, retries for failed steps, logging for exceptions, and detection of CAPTCHAs.
This step ensures the bot can handle unexpected changes without crashing.

### Phase 5 — Database Layer
Integrated PostgreSQL to store flight searches and booking confirmations.
Used SQLAlchemy models for `flights` and `bookings`.
This step allows structured data storage, retrieval, and further analysis.

### Phase 6 — Dockerization
Dockerized the app and PostgreSQL database using `Dockerfile` and `docker-compose.yml`.
The bot can run anywhere with a single command, simplifying deployment and testing.

### Phase 7 — Testing
Implemented unit tests for database operations and mocked Selenium flows using `pytest`.
Added optional GitHub Actions CI to run tests automatically.
This step ensures code reliability and maintainability.

### Phase 9 — Configuration Management

Separated secrets and settings from code using .env files and pydantic settings.
Centralized database URLs, browser options, and other configs for easier management.
This step improves security, flexibility, and portability across local, Docker, and CI/CD environments.

### Phase 10 — Logging & Monitoring

Added structured logging with log levels and timestamps.
Prepared monitoring hooks for future integration with Prometheus or ELK.
This step improves visibility into the bot’s operations and helps with debugging.

### Phase 11 — Advanced Testing

Implemented headless Selenium and integration tests with a Dockerized PostgreSQL.
Added code coverage reports using pytest-cov.
This step ensures end-to-end reliability and demonstrates professional testing practices.

### Phase 13 — CI/CD Enhancements

Integrated GitHub Actions to run automated tests, linting, and optionally Docker builds on every push or pull request.
Installed project dependencies using uv to ensure environment consistency.
This step ensures code quality, maintains reliability, and demonstrates professional DevOps practices.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (if running locally)

### Clone the Repo
```bash
git clone https://github.com/besleagadan/travel-booking-bot.git
cd travel-booking-bot
```

## Local Run
```bash
uv run -m app.main
```

## Docker Run
```bash
docker-compose up --build
```

## Example Output

### Flight search results:
```json
{'flight': 'UA954', 'airline': 'United Airlines', 'price': '$400'}
{'flight': 'LH123', 'airline': 'Lufthansa', 'price': '$500'}
```

### Booking confirmation:
```yaml
Booking Status: Thank you for your purchase today!
Booking ID: 12345
Price: 400 USD
```

## Tests

### Run unit tests:
```bash
uv run pytest
```

### Example output:
```bash
tests/test_db.py ..                         [100%]
```

### Run tests with coverage:
```bash
uv run pytest --cov=app tests/
```

### Example output:
```bash
---------- coverage: platform linux, python 3.11 ----------
Name              Stmts   Miss  Cover
-------------------------------------
app/db.py            25      0   100%
app/scraping.py      40      2    95%
```



