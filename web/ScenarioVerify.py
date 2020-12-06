from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import os
from ContainerCommit import containercommit
import fnmatch
import subprocess

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

containerverify = Blueprint('containerverify', __name__)

@containerverify.route('/verify', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        client = docker.from_env()
        ContainerName = session['user']
        g.csID = session['user']
        command = client.containers.get(g.csID)
        apache2 = command.exec_run('dpkg -l')
        # ListWeb = 'apache2'
        # filtered = fnmatch.filter(apache2, 'apache?') 
        output = subprocess.check_output(['dpkg', '-l'])
        for output in apache2.split('\n'):
            print(output)        
    else:
        return redirect('/login')

