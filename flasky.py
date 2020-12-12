import os
from app import run

ENV = "development"
SELECTED_ENV = os.getenv("FLASK_ENV")

if SELECTED_ENV is not None:
    if SELECTED_ENV == "production":
        ENV = "production"

app = run(ENV)


