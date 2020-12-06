# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import datetime
import os
from ContainerPush import containerpush

app = Flask(__name__)
app.secret_key = "10pearls" 
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

# Blue print declearation
containercommit = Blueprint('containercommit', __name__)

# Route Defination 
@containercommit.route('/commit')
def index():
    if session.get('loggedin') is not None:
        containerSessionID = session['user']
        g.csID = session['user']
        registryName = app.config.get("REGISTRY")
        ImageName = registryName + '/' + containerSessionID
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%b%d")
        client = docker.from_env()
        container = client.containers.get(containerSessionID)
        print("Start commiting your docker image...")
        container.commit(repository=containerSessionID, tag=timestamp)
        client.containers.get(containerSessionID) 
        container.stop()
        container.remove()
        print("Image has been commited")
        return containerpush.pushImage()
    else:
        return render_template('index.html')
