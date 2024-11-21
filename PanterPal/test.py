# This should only be run once to create the tables
from model import db
db.create_all()  # Create tables based on your models
