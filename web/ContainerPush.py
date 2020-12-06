from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests

containerpush = Blueprint('containerpush', __name__)

@containerpush.route('/scene1')
def index():
    if session.get('loggedin') is not None:
        print('Starting pushing docker image')
        client = docker.from_env()
        client.images.push(repository='mansurali901/test')
    else:
        return render_template('index.html')