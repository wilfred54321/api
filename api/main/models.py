from api import db
from datetime import datetime



class Joke(db.Model):
    __tablename__ = 'jokes'
    joke_id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String, nullable = False)
    answer = db.Column(db.String,nullable = False)
