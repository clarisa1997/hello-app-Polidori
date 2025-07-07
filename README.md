# hello-app

A Docker-based demo project that shows a web page with a personalized message:

> **Hello world, Clarissa!**

The name is retrieved from a PostgreSQL database via a Flask backend, and displayed using a Flask frontend.

---

## Application Features

The frontend is a Flask application that shows a greeting message on the main page (`/`). It queries the backend service to get the name, which is fetched from the PostgreSQL database. If the backend is unreachable or returns an error, the frontend shows an error message.

---

## Project Structure

```bash
hello-app
├── backend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── database
│   ├── Dockerfile
│   └── init.sql
├── frontend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── secrets
│   └── db_password.txt
├── tests
│   ├── test_backend.py
│   ├── test_frontend.py
│   └── test_frontend_mock.py
├── .env
├── docker-compose.yml
├── Makefile
├── requirements-dev.txt
├── start.sh
├── stop.sh
└── README.md
```

- `frontend`: contains the source code of the frontend application.  
- `backend`: contains the source code of the backend application.  
- `database`: contains the PostgreSQL initialization script and Dockerfile.  
- `secrets`: stores sensitive information such as the database password.  
- `tests`: contains tests for frontend and backend.  
- `docker-compose.yml`: defines the services and how they are connected.  
- `.env`: environment variables configuration file.  
- `Makefile`: shortcuts for building, running, stopping, testing, and linting.  
- `requirements-dev.txt`: development dependencies (testing, linting).  
- `start.sh` and `stop.sh`: scripts to start and stop the project containers.  
- `README.md`: this file.

---

## Prerequisites

- Docker and Docker Compose (v2) installed.  
- Git installed to clone the repository.  
- Python 3.11+ (for running tests locally).  
- pip package manager.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/clarisa1997/hello-app-Polidori.git
cd hello-app-Polidori
```

### 2. Create the `db_password.txt` file

The `db_password.txt` file contains the PostgreSQL database password. For security reasons, it is **not included** in the repository and must be created manually in the `secrets/` directory:

```bash
echo "your_db_password" > secrets/db_password.txt
```

### 3. Create the `.env` file

Create a `.env` file in the project root with the following environment variables:

```env
WEB_PORT=8000
BACKEND_ALIAS=backend
BACKEND_PORT=5000

DB_NAME=mydb
DB_USER=myuser
DB_HOST=database
DB_PASSWORD_FILE=/run/secrets/db_password

POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=your_db_password
```

Adjust values as needed.

### 4. Build and start the application

Start all services with:

```bash
./start.sh
```

Alternatively, you can run:

```bash
make build
make up
```

### 5. Access the frontend

Open your browser and go to:

```
http://localhost:8000
```

You should see:

```
Hello world, Clarissa Polidori!
```

---

## Stopping the services

To stop and remove containers and networks, run:

```bash
./stop.sh
```

Or:

```bash
make down
```

---

## Running Tests

Tests are implemented using `pytest`. You can run all tests by executing:

```bash
make test
```

Or manually:

```bash
pytest tests/
```

### Test files overview

| File                    | Description                                                    |
|-------------------------|----------------------------------------------------------------|
| `test_backend.py`       | Tests backend API endpoint `/name`.                            |
| `test_frontend.py`      | Tests frontend displays greeting correctly.                   |
| `test_frontend_mock.py` | Tests frontend handling of backend failure scenarios.         |

---

## Code Linting

Ensure code style with:

```bash
make lint
```

---

## Debugging and Logs

View logs from all running containers using:

```bash
make logs
```

---

## Security Considerations

- Database password is stored securely using Docker Secrets.  
- `.env` and `secrets/` directories are excluded from version control via `.gitignore`.  
- Environment variables are centralized and configurable in the `.env` file.

---

## Technologies Used

- Docker & Docker Compose (v2)  
- Python 3.11+  
- Flask for backend and frontend  
- PostgreSQL database  
- pytest for testing  
- flake8 for linting  
- Makefile and Bash scripts for automation

---

## Author

Clarissa Polidori.