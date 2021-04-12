from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import os

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

# Container Bluprint Initializer
containerpush = Blueprint('containerpush', __name__)

@containerpush.route('/push', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        client = docker.from_env()
        ContainerName = session['user']
        g.csID = session['user']
        registryName = app.config.get("REGISTRY")
        ImageName = registryName + '/' + ContainerName
        print('Starting pushing docker image')
        client.images.push(repository=ImageName)
    else:
        return redirect('/login')