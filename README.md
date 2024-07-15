# Flask OpenAI Chat Application

This repository contains a Flask application that uses OpenAI's API for chat functionality.<br>
It includes SQLAlchemy for database management, Alembic for migrations, Docker for containerization and pytest for testing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)

## Prerequisites

- Python 3.9
- PostgreSQL
- Docker & Docker Compose

## Setup Instructions

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
- Windows:
    ```bash
    venv\Scripts\activate
    ```

- MacOS/Linux:
    ```bash
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create two files for environment variables:**

- .env.local:
    ```bash
    SQLALCHEMY_DATABASE_URI=postgresql://<username>:<password>@localhost/<db_name>
    OPENAI_API_KEY=<your_openai_api_key>
    FLASK_APP=app.py
    FLASK_RUN_HOST=0.0.0.0
    FLASK_ENV=development
    ```

- .env.docker:
    ```bash
    SQLALCHEMY_DATABASE_URI=postgresql://<username>:<password>@db:5432/<db_name>
    OPENAI_API_KEY=<your_openai_api_key>
    POSTGRES_USER=<your_username>
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_DB=<your_db_name>
    FLASK_ENV=docker
    FLASK_APP=app.py
    FLASK_RUN_HOST=0.0.0.0
    ```

## Running the Application

1. **Run the Flask application locally:**

- Apply the migration: (just once)
    ```bash
    alembic upgrade head
    ```

- Run the application:
    ```bash
    flask run
    ```

2. **Running the application in Docker:**

- Build the Docker image: (just once)
    ```bash
    docker-compose build
    ```

- Start the Docker container:
    ```bash
    docker-compose up
    ```

- Apply the migration: (just once)
    ```bash
    docker-compose exec web alembic upgrade head
    ```

## Testing the Application

1. **Run the tests locally:**
    ```bash
    pytest
    ```

2. **Run the tests in Docker:**
    ```bash
    docker-compose exec web pytest
    ```
