# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, g
import docker
from docker import client
from flask_session import Session
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

# Blueprints import here 
from ContainerCommit import containercommit
from containerCreate import containercreate
from ScenarioVerify import containerverify

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls"  

# Loading all Blueprints 
app.register_blueprint(containercommit)
app.register_blueprint(containercreate)
app.register_blueprint(containerverify)

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

# Enter your database connection details below
app.config['MYSQL_HOST'] = app.config.get("MYSQL_HOST_IP")
app.config['MYSQL_USER'] = app.config.get("MYSQL_USER")   
app.config['MYSQL_PASSWORD'] = app.config.get("MYSQL_PASS")
app.config['MYSQL_DB'] = app.config.get("AUTHDB")

# # Callable Properties 
dockerRegistry = app.config.get("REGISTRY")
dockerUsername = app.config.get("DOCKER_USER")
dockerPassword = app.config.get("DOCKER_PASSWORD")   

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    if session.get('loggedin') is not None:
        return render_template('welcome.html')
    else:    
        return render_template('index.html')

@app.route('/welcome')
def welcome():
    if session.get('loggedin') is not None:
        return render_template('welcome.html',user=session['user'])  # render a template
    else:
        return render_template('index.html')

## Session Token generation after login
@app.before_request
def before_request():
    g.user = None
    g.hostip = None
    if 'username' in session:
        session['user'] = session['username']

# Scenario pages 
@app.route('/scenario')
def scenarioOne ():
    if session.get('loggedin') is not None:
        return render_template('scenarios.html')
    else:
        return render_template('index.html')
# SSH Docker container IP
# This function generate or get IP Docker Container IP

@app.route('/Connect')
def ConnectInfo():
    if session.get('loggedin') is not None:
        ContainerName = None
        ContainerIP = None
        ip_add = None
        ContainerName = session['user']
        client = docker.DockerClient()
        container = client.containers.get(session['user'])
        ContainerIP = container.attrs['NetworkSettings']['IPAddress']
        return ContainerIP
        g.hostip = ContainerIP
    else:
        return render_template('index.html')
# Rendering page for docker container ssh 
@app.route('/ssh')
def connectrout ():
    if session.get('loggedin') is not None:
        hostip = ConnectInfo()
        return render_template('ssh.html', hostip=hostip)
    else:
        return render_template('index.html')

# Login Section
@app.route('/login', methods=['GET', 'POST'])
def index():
    msg = ''
    error = None
    user = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
    # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            # Redirect to home page
            return render_template('welcome.html', msg=msg)

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)
  
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

