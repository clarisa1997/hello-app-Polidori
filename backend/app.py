# Import required libraries
from flask import Flask
import os
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)


# Function to establish a connection to the PostgreSQL database
def create_conn():
    conn = None
    # Read the database password from a secure file (Docker Secret)
    db_password_file = os.getenv("DB_PASSWORD_FILE",
                                 "/run/secrets/db_password")
    with open(db_password_file, "r") as file:
        db_password = file.read().strip()
    try:
        # Connect to the database using credentials from environment variables
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", default="mydb"),
            user=os.getenv("DB_USER", default="myuser"),
            password=db_password,
            host=os.getenv("DB_HOST", default="localhost"),
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn


# API route that fetches the first user's name from the DB
@app.route("/name")
def get_name():
    conn = create_conn()
    if conn is None:
        return "-1"
    cur = conn.cursor()
    cur.execute("SELECT name FROM users LIMIT 1;")
    name_res = cur.fetchone()[0]
    conn.close()
    return name_res


# Start the Flask application
if __name__ == "__main__":
    app.run(
        host=os.getenv("BACKEND_HOST", default="0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", default=5000)),
    )
