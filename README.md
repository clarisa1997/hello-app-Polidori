# hello-app

A Docker-based demo project that shows a web page with a personalized message:

> **Hello world, Clarissa!**

The name is retrieved from a PostgreSQL database via a Flask backend, and displayed using a Flask frontend.

---

## Architecture

```
[ frontend (Flask) ]  --->  [ backend (Flask API) ]  --->  [ database (PostgreSQL) ]
```

- **Frontend**: displays the web page and queries the backend via HTTP  
- **Backend**: a Flask API that retrieves the name from the database  
- **Database**: PostgreSQL container with initial data (name)  

---

## Requirements

- Docker  
- Docker Compose (v2)  
- Make (optional but recommended)  
- Bash (Linux/macOS or WSL on Windows)  

---

## Project structure


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
│   ├── unit_test_backend.py
│   ├── unit_test_frontend.py
│   ├── unit_test_e2e.py
│   └── requirements.txt
├── .env
├── docker-compose.yml
├── Makefile
├── start.sh
├── stop.sh
└── README.md

- `frontend`: contains the source code of the frontend application.  
- `backend`: contains the source code of the backend application.  
- `database`: contains the PostgreSQL initialization script and Dockerfile.  
- `secrets`: stores sensitive information such as the database password.  
- `tests`: contains unit and end-to-end tests for frontend and backend.  
- `docker-compose.yml`: defines the services and how they are connected.  
- `.env`: environment variables configuration file.  
- `Makefile`: shortcuts for building, running, stopping, linting, and testing.  
- `start.sh` and `stop.sh`: scripts to start and stop the application containers.  
- `README.md`: this file.  
```
---

## Quick start

### 1. Clone or extract the project

```bash
git clone https://github.com/clarisa1997/hello-app-Polidori.git
cd hello-app
```

### 2. Create the `db_password.txt` file

```bash
mkdir -p secrets
echo "your_db_password" > secrets/db_password.txt
```

### 3. Create the `.env` file

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

### 4. Build and start the application

```bash
./start.sh
```

Alternatively:

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
Hello world, Clarissa!
```

---

## Testing & Linting

We maintain three core test suites—each running in disposable Python containers so you never need to install anything on your host:

### 1. Backend Unit Tests (`tests/unit_test_backend.py`)
- **What it covers**  
  - `create_conn()` under both successful and `OperationalError` conditions (mocks `psycopg2.connect`).  
  - `get_name()` when a valid connection returns a name, and when the connection is `None`.  
- **Why it matters**  
  Validates your database-access logic in isolation, ensuring connection setup and query handling are rock-solid before hitting a real DB.

### 2. Frontend Unit Tests (`tests/unit_test_frontend.py`)
- **What it covers**  
  - The Flask `/` route returns **“Hello world, {name}!”** when `get_name()` succeeds (mocked to return a sample name).  
  - It shows **“There was an error getting the name”** when `get_name()` returns `-1`.  
- **Why it matters**  
  Checks your UI behavior without launching any HTTP servers—your rendering logic and error handling get thoroughly verified.

### 3. End-to-End Smoke Tests (`tests/test_e2e.py`)
- **What it covers**  
  - Polls the live backend at `http://localhost:5000/name` until it responds, then asserts a non-empty name.  
  - Polls the live frontend at `http://localhost:8000/` until it serves a page containing **“Hello world”**.  
- **Why it matters**  
  Exercises the full stack (DB → backend → frontend) over real HTTP, ensuring your Compose setup and port mappings work as expected.

#### How to run the tests

1. **Start your application stack**  
   ```bash
   make build && make up
   ```

2. **Lint your code**  
   ```bash
   make lint
   ```  
   - Runs `flake8` inside a temporary `python:3.11-slim` container with dev deps.

3. **Run all tests**  
   ```bash
   make test
   ```  
   - Runs `pytest` inside a temporary `python:3.11-slim` container (with `--network host`), installing runtime & dev deps.

4. **Tear down**  
   ```bash
   make down
   ```

---

## Security

- The database password is not written in the code but stored in `secrets/db_password.txt` and injected via Docker Secrets.  
- `.env` and `secrets/` are excluded from Git via `.gitignore`.

---

## Technologies Used

- Docker & Docker Compose (v2)  
- Python 3.11+, Flask  
- PostgreSQL  
- pytest, flake8, requests  
- Makefile and Bash scripts  

---

## Author

Clarissa Polidori — Cloud-engineer-graduate-ION-project.  