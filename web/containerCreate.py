from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
from flask import flash

containercreate = Blueprint('containercreate', __name__)

@containercreate.route('/scene1', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        client = docker.from_env()
        ContainerName = session['user']
        container = client.containers.run('openssh:1.0.0', '/bin/sleep 10800', detach=True, name=ContainerName, environment=['env=DEV', 'ROOT_PASS=mypass'])
        commandContainer = client.containers.get(ContainerName)
        commandContainer.exec_run('service ssh start', stdout=True)
        flash('Container has been container')
        
        return render_template('layout.html')
    else:
         return redirect('/login')  