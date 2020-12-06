from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import os
from ContainerCommit import containercommit
#from app import Debug 

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

containerverify = Blueprint('containerverify', __name__)

@containerverify.route('/verify')
def index():
    # client = docker.from_env()
    # ContainerName = session['user']
    # g.csID = session['user']
    # registryName = app.config.get("REGISTRY")
    # ImageName = registryName + '/' + ContainerName
    # return ImageName

    print(dockerRegistry)
    return Debug()   


