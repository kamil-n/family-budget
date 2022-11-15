import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
