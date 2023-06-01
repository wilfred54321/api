import csv

import flask

from api.main.models import Joke
from api import db
import random
from flask import make_response,jsonify,request
from flask_login import current_user

from flask import Blueprint

jokes = Blueprint('jokes', __name__)

@jokes.route("/")
def index():
    return "This is the jokes index route"


@jokes.route("/import")
def import_jokes():

    with open("assets/jokes.csv") as file:
        count = 0
        data = csv.reader(file)
        for joke_id,question,answer in data:
            joke = Joke(
                joke_id = joke_id,
                question=question,
                answer=answer
            )
            db.session.add(joke)
            count += 1
    db.session.commit()
    message = f"{count} jokes added successfully"
    return message

@jokes.route("/random/joke",methods = ["GET"])
def get_random_joke():

    joke_id = random.randrange(1,200)
    joke = Joke.query.filter_by(joke_id = joke_id).first()
    joke = {'joke_id':joke.joke_id,
            'question':joke.question,
            'answer':joke.answer}

    #return a list of keys of a specific user
    # get the user email from the request header
    #get the list of keys associated with that user
    #set the server response key to the keys associated with the user
    #check if the request key match with the response key
    keys = ['thisismyapikey','thisismyapikey2','thisismyapikey3']

    response =  make_response(jsonify(joke),200)
    response.headers['key'] = keys

    response.headers['host'] = "http://wilfredapi.net"

    if (request.headers.get('Key') in (response.headers.getlist('key')[0]))\
        and (request.headers.get('host') in list(response.headers.values())):
        return response
    return make_response("Not authorized,Ensure you have a valid api key and the correct host is specified",401)

    # resp = flask.Response(joke)
    # resp.headers["this is a header content"]='*'
    # return resp
