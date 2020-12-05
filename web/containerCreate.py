from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests

containercreate = Blueprint('containercreate', __name__)

@containercreate.route('/scene1')
def index():
    client = docker.from_env()
    ContainerName = session['user']

    container = client.containers.run('openssh:1.0.0', '/bin/sleep 10800', detach=True, name=ContainerName, environment=['env=DEV', 'ROOT_PASS=mypass'], ports={'22/tcp':1222})
    return render_template('ssh.html')