# Import required libraries
from flask import Flask
import os
import requests

app = Flask(__name__)


# Function to request the name from the backend service
def get_name():
    try:
        # Call the backend endpoint to get the name
        response = requests.get(
            f'http://{os.getenv("BACKEND_ALIAS", default="localhost")}:'
            f'{os.getenv("BACKEND_PORT", default="5001")}/name',
            timeout=5,
        )
        response.raise_for_status()
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ) as e:
        print("Error occurred:", e)
        return -1
    return response.text


# Main route displaying "Hello world, {name}"
@app.route("/")
def hello_world():
    name = get_name()
    if name == -1:
        return "There was an error getting the name"
    return f"Hello world, {name}!"


# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("WEB_PORT", default="8000")))
