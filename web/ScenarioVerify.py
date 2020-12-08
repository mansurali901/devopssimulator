from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import os
from ContainerCommit import containercommit
import io
from contextlib import redirect_stdout

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

containerverify = Blueprint('containerverify', __name__)

@containerverify.route('/verify', methods=['GET', 'POST', 'UPDATE'])
def apache2():        
    if session.get('loggedin') is not None:
        client = docker.from_env()
        ContainerName = session['user']
        g.csID = session['user']
        command = client.containers.get(g.csID)
        firstString = []
        apache2 = command.exec_run("dpkg -l apache2")
        list_string = str(apache2)
        final = list_string.find('code=0')
        if final > 0:
            print('Package is installed')
        else:
            print('Not Installed')
        return 'end'       
    else:
        return redirect('/login')



