# Urban Transit Facilities - Documentation Guide

## 1. Project Overview

Urban Transit Facilities is a Django-based web application designed to manage various aspects of urban transit operations. Key features include:

*   User account management (`accounts` app)
*   Location tracking and management (`locations` app)
*   Inventory management (e.g., vehicles) (`inventory` app)
*   Service provider information (`providers` app - inferred from `settings.py`)
*   Charging and rate management (`charges` app)
*   A user interface (`ui` app)
*   A RESTful API for programmatic access (built with Django REST Framework).
*   Asynchronous task processing using Celery.
*   API documentation via Swagger/OpenAPI (available at `/api/docs/` in development).

## 2. Development Environment Setup

These instructions expand upon the existing `README.md`.

### 2.1. Prerequisites

*   **Python 3.x**: Ensure Python 3 is installed on your system.
*   **pip**: Python package installer.
*   **virtualenv**: For creating isolated Python environments.
*   **Git**: For version control.
*   **PostgreSQL**: Required for staging and production environments. For development, SQLite is used by default, but you might want to set up PostgreSQL to mirror production more closely.
*   **Redis (or RabbitMQ)**: Required as a message broker for Celery. The choice of broker might be specified elsewhere or assumed (Redis is common).

### 2.2. Initial Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/transport-stack/urban-transit-facilities.git
    cd urban-transit-facilities
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Ensure python3-venv is installed (as per original README)
    # sudo apt install python3-venv # Uncomment if not installed
    python3 -m venv venv
    source venv/bin/activate
    ```
    *On Windows, activation is `venv\Scripts\activate`*

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install Django, Celery, Django REST Framework, psycopg2 (if you intend to use PostgreSQL), and other necessary packages.

### 2.3. Environment Variables

This project uses a `.env` file to manage environment-specific configurations. A sample file `.env.sample` is provided.

1.  **Create a `.env` file:**
    Copy `.env.sample` to `.env` in the project root:
    ```bash
    cp .env.sample .env
    ```

2.  **Configure variables in `.env`:**
    Open the `.env` file and fill in the required values:

    ```dotenv
    SECRET_KEY="your_strong_random_secret_key"  # Important: Generate a new strong key for production
    EMAIL_HOST_USER="your_email@example.com"
    EMAIL_HOST_PASSWORD="your_email_password"
    ALLOWED_HOSTS="127.0.0.1 localhost your_domain.com" # Space-separated list

    # Database Configuration (PostgreSQL for Staging/Prod, SQLite for Dev by default)
    # If using PostgreSQL in development, set IS_DEV=False and configure these:
    DB_NAME="urban_transit_db"
    DB_USER="your_db_user"
    DB_PASS="your_db_password"
    # DB_HOST and DB_PORT can be added if not 'localhost' and '5432'

    # Environment Flags (set one to "True", others to "False")
    IS_DEV="True"         # For local development (uses SQLite, DEBUG=True)
    IS_STAG="False"        # For staging environment (uses PostgreSQL, DEBUG=True)
    IS_PROD="False"        # For production environment (uses PostgreSQL, DEBUG=False)

    GMAPS_KEY="your_google_maps_api_key" # If Google Maps integration is used

    # ELK Stack (Elasticsearch, Logstash, Kibana) & APM Configuration
    ELK_SECRET_TOKEN="your_elk_secret_token" # If used
    ELK_SERVER_URL="your_elk_server_url"     # If used
    ELASTIC_APM_ENABLED="False"             # Set to "True" to enable APM

    # CSRF Trusted Origins (if your app is served under different domains/ports)
    # Example: CSRF_TRUSTED_ORIGINS="https://your_domain.com,http://localhost:3000"
    CSRF_TRUSTED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
    ```

    **Important Notes:**
    *   For `IS_DEV="True"`, the application will use SQLite (`db.sqlite3`) by default, and `SECRET_KEY` will be a default insecure key (fine for local dev).
    *   For `IS_STAG="True"` or `IS_PROD="True"`, you **must** provide a strong `SECRET_KEY` and PostgreSQL database credentials (`DB_NAME`, `DB_USER`, `DB_PASS`).
    *   `ALLOWED_HOSTS` should be a space-separated list of hostnames/IPs the Django site can serve.

### 2.4. Database Setup

1.  **For Development (SQLite - default):**
    No specific database creation steps are needed if `IS_DEV="True"`. Django will create `db.sqlite3` automatically.

2.  **For Staging/Production (PostgreSQL):**
    *   Ensure PostgreSQL server is installed and running.
    *   Create a database and a user with privileges for this database, matching the credentials in your `.env` file.
        ```sql
        -- Example PostgreSQL commands:
        CREATE DATABASE urban_transit_db;
        CREATE USER your_db_user WITH PASSWORD 'your_db_password';
        GRANT ALL PRIVILEGES ON DATABASE urban_transit_db TO your_db_user;
        ALTER ROLE your_db_user SET client_encoding TO 'utf8';
        ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE your_db_user SET timezone TO 'UTC';
        ```

### 2.5. Running Migrations

Once the database is configured (or for SQLite, ready to be created), apply the database migrations:

```bash
python manage.py migrate
```
This command creates the necessary database tables based on your project's models.

### 2.6. Creating a Superuser (Admin User)

To access the Django admin interface (`/admin/`):

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 2.7. Loading Initial Data (Fixtures)

The `README.md` provides commands to load initial data. This is crucial for populating lookup tables and default settings.

```bash
python manage.py loaddata locations/fixtures/country.json
python manage.py loaddata locations/fixtures/states.json
python manage.py loaddata locations/fixtures/pincode.json
python manage.py loaddata inventory/fixtures/vehicletype.json
python manage.py loaddata charges/fixtures/paymentmode.json
python manage.py loaddata main/fixtures/days.json
python manage.py loaddata main/fixtures/settings.json
```
*(Ensure these fixture files exist at the specified paths)*

## 3. Running the Application

### 3.1. Starting the Django Development Server

```bash
python manage.py runserver
```
By default, the server will run at `http://127.0.0.1:8000/`.
You can specify a different port: `python manage.py runserver 0.0.0.0:8080` (to make it accessible on your local network).

### 3.2. Running Celery (for Asynchronous Tasks)

If your project uses Celery for background tasks, you'll need to run a Celery worker and Celery Beat (for scheduled tasks).

1.  **Ensure a message broker (e.g., Redis) is running.**
    *   Install Redis: `sudo apt install redis-server` (or use Docker/other methods).
    *   Start Redis: `sudo systemctl start redis-server`.

2.  **Run the Celery worker:**
    Open a new terminal, activate the virtual environment, and run:
    ```bash
    celery -A core worker -l info
    ```
    *(Replace `core` with the name of your Django project application where Celery is initialized if different, but `core` is likely correct given `core.settings`)*

3.  **Run Celery Beat (for scheduled tasks):**
    Open another new terminal, activate the virtual environment, and run:
    ```bash
    celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ```

## 4. Optional Tools and Services

*   **PostgreSQL**: While SQLite is used for `IS_DEV=True`, using PostgreSQL locally can help catch database-specific issues early. Install PostgreSQL and the `psycopg2-binary` package (`pip install psycopg2-binary`).
*   **Redis**: Commonly used as a Celery message broker and for caching. Install Redis server.
*   **Elastic APM Server**: If `ELASTIC_APM_ENABLED="True"`, you'll need an Elastic APM server instance to send data to. Configure `ELK_SERVER_URL` and `ELK_SECRET_TOKEN` in `.env`.
*   **Mail Server/Service**: For email functionalities (e.g., password reset, notifications), ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correctly set up for a service like SendGrid, Mailgun, or a local SMTP server for testing (like `python -m smtpd -c DebuggingServer -n localhost:1025`).

## 5. API Documentation

When `DEBUG` is true (e.g., `IS_DEV="True"` or `IS_STAG="True"`), API documentation is available through `drf-spectacular`:

*   **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
*   **ReDoc UI**: `http://127.0.0.1:8000/api/docs/redoc/`
*   **Schema Download**: `http://127.0.0.1:8000/api/`

## 6. Running Tests

The project is configured to use `pytest` and `pytest-django`.

To run all tests:

```bash
pytest
```

To run tests for a specific app:

```bash
pytest accounts/
```

(See section below for writing basic tests).

## 7. Project Structure Highlights

*   `core/`: Contains main project settings (`settings.py`), URL configurations (`urls.py`), and `wsgi.py`.
*   `manage.py`: Django's command-line utility.
*   `requirements.txt`: Python dependencies.
*   `.env.sample`: Template for environment variables.
*   `README.md`: Basic project information.
*   **Apps** (`accounts/`, `locations/`, `inventory/`, `providers/`, `charges/`, `main/`, `ui/`):
    *   Each app typically contains `models.py`, `views.py`, `urls.py` (for app-specific routes), `admin.py`, `tests.py`, and potentially `serializers.py` (for DRF).
*   `templates/`: Project-level HTML templates.
*   `static/`: Project-level static files (CSS, JS, images).

This documentation provides a comprehensive guide to setting up, running, and understanding the Urban Transit Facilities project. Refer to individual app directories and Django/DRF documentation for more specific details.
