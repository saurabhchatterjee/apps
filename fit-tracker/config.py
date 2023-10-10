import datetime
import hashlib
from os import path, environ
from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))
uri = path.join(basedir, 'database.db')
secret_sauce = "my calorie logger"


# data = datetime.date.today().strftime("%a %b %d %Y") + secret_sauce


def create_hash(today):
    hash_input = today.strftime("%a %b %d %Y") + secret_sauce
    hash_object = hashlib.sha256()
    hash_object.update(hash_input.encode('utf-8'))
    return hash_object.hexdigest()


# # Create a hashlib object for the hash function you want to use
# hash_object = hashlib.sha256()
#
# # Update the hash object with the bytes of the data you want to hash
# hash_object.update(data.encode('utf-8'))
#
# # Get the hexadecimal representation of the hash
# hashed_data = hash_object.hexdigest()


class Config:
    """Set Flask configuration vars from .env file."""
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    # Database
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{uri}'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # FACTS
    DB_HASH = create_hash(datetime.date.today())
    TODAY = datetime.date.today().strftime("%a %b %d %Y")
