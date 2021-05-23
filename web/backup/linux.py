import MySQLdb 
from flask import Flask, render_template 
from flask_session import Session
import requests
import datetime
from ContainerPush import containerpush
from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import os
from ContainerCommit import containercommit
from dbconnection import connection # DB connection Module 

app = Flask(__name__)
app.secret_key = "10pearls" 
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)


# Blue print declearation 
linuxtask = Blueprint('linuxtask', __name__)

@linuxtask.route('/linux', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        #hostip = ConnectInfo()
        stageMode = 'mysql'
        session['stage'] = stageMode  
        return render_template('mysql.html')
    else:
        return redirect('/login')