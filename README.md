# Flask OpenAI Chat Application

This repository contains a Flask application that uses OpenAI's API for chat functionality.<br>
It includes SQLAlchemy for database management, Alembic for migrations, Docker for containerization and pytest for testing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Virtual Environment](#virtual-environment)
  - [Environment Variables](#environment-variables)
  - [Database Migrations](#database-migrations)
  - [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)

## Prerequisites

- Python 3.9
- PostgreSQL
- Docker & Docker Compose

## Setup Instructions

### Virtual Environment

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

### Environment Variables

Create two files: .env.local and .env.docker

1. **.env.local:**
    ```bash
    SQLALCHEMY_DATABASE_URI=postgresql://<username>:<password>@localhost/<db_name>
    OPENAI_API_KEY=<your_openai_api_key>
    ```

2. **.env.docker:**
    ```bash
    SQLALCHEMY_DATABASE_URI=postgresql://<username>:<password>@db:5432/<db_name>
    OPENAI_API_KEY=<your_openai_api_key>
    POSTGRES_USER=<your_username>
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_DB=<your_db_name>
    FLASK_ENV=docker
    ```

### Database Migrations

1. **Initialize Alembic:**
    ```bash
    alembic init migrations
    ```

2. **Configure alembic to use SQLAlchemy:**
- Remove the hardcoded URL from alemic.ini:
    ```bash
    sqlalchemy.url = driver://user:pass@localhost/dbname
    ```

- Replace the code in migrations/env.py:
    ```python
    from alembic import context
    from sqlalchemy import engine_from_config, pool
    from logging.config import fileConfig
    from dotenv import load_dotenv
    from models import db
    import os

    if os.getenv('FLASK_ENV') == 'docker':
        load_dotenv('.env.docker')
    else:
        load_dotenv('.env.local')

    config = context.config
    fileConfig(config.config_file_name)
    config.set_main_option('sqlalchemy.url', os.getenv('SQLALCHEMY_DATABASE_URI'))
    target_metadata = db.metadata

    def run_migrations_offline():
        """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well. By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.

        """
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url, target_metadata=target_metadata, literal_binds=True
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online():
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)

            with context.begin_transaction():
                context.run_migrations()

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
    ```

4. **Create the initial migration:**
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```

5. **Apply the migration:**
    ```bash
    alembic upgrade head
    ```

### Docker Setup

1. **Build the Docker image:**
    ```bash
    docker-compose build
    ```

2. **Start the Docker container:**
    ```bash
    docker-compose up
    ```

3. **Create the database tables:**
    ```bash
    docker-compose exec web alembic upgrade head
    ``` 

## Running the Application

- **Run the Flask application locally:**
    ```bash
    flask run
    ```

- Running the application in Docker:
    ```bash
    docker-compose up
    ```

## Testing the Application

- **Run the tests:**
    ```bash
    pytest
    ```

- **Run the tests in Docker:**
    ```bash
    docker-compose exec web pytest
    ```