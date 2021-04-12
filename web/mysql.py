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
mysqltask = Blueprint('mysqltask', __name__)

@mysqltask.route('/mysql', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        hostip = ConnectInfo()
        return render_template('mysql.html')
    else:
        return redirect('/login')
        
def ConnectInfo():
    if session.get('loggedin') is not None:
        ContainerName = None
        ContainerIP = None
        ip_add = None
        ContainerName = session['user']
        client = docker.DockerClient(base_url='tcp://192.168.1.104:2375')
        # client = docker.DockerClient()
        container = client.containers.get(session['user'])
        ContainerIP = container.attrs['NetworkSettings']['IPAddress']
        return ContainerIP
        g.hostip = ContainerIP
    else:
        return redirect('/login')
        
