from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint, abort
from flask import request, jsonify
from flask_session import Session
import requests

# This file is for learning JSON based API
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': u'A Fire Upon the Deep',
     'author': u'Vernor Vinge',
     'first_sentence': u'The coldsleep itself was dreamless.',
     'year_published': u'1992'},
    {'id': 1,
     'title': u'The Ones Who Walk Away From Omelas',
     'author': u'Ursula K. Le Guin',
     'first_sentence': u'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': u'1973'},
    {'id': 2,
     'title': u'Dhalgren',
     'author': u'Samuel R. Delany',
     'first_sentence': u'to wound the autumnal city.',
     'published': u'1975'}
]

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
resultGet = Blueprint('resultGet', __name__)
@resultGet.route('/api', methods=['GET'])
def api_all():
    return jsonify(tasks)

resultGetbyID = Blueprint('resultGetbyID', __name__)
@resultGetbyID.route('/api/resultGetbyID/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in books if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# POST API 
resultPOST = Blueprint('resultPOST', __name__)
@resultPOST.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201