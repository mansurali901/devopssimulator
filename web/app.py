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
from dbconnection import connection # DB connection Module 


# Blueprints import here 
from ContainerCommit import containercommit
from containerCreate import containercreate
from ScenarioVerify import containerverify
from logout import logout
from resultGet import resultGet, resultGetbyID, resultPOST
from resultPost import resultpost
from mysql import mysqltask
from VerifyModule import mysqlverify

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls"  

# Loading all Blueprints 
app.register_blueprint(containercommit)
app.register_blueprint(containercreate)
app.register_blueprint(containerverify)
app.register_blueprint(logout)
app.register_blueprint(resultGet)
app.register_blueprint(resultGetbyID)
app.register_blueprint(resultPOST)
app.register_blueprint(resultpost)
app.register_blueprint(mysqltask)
app.register_blueprint(mysqlverify)

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
dockerHost = app.config.get("DOCKER_HOST") 

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST', 'UPDATE'])
def home():
    if session.get('loggedin') is not None:
        # HTML_File=open('welcome.html','r')
        # s = HTML_File.read().format(p=())

        #index = open("welcome.html").read().format(username=session['user'])
        return render_template('welcome.html')
        #return index
    else:    
        return redirect(url_for('/login')) 

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
        c, conn = connection()  
#        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        c.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        rows = [c.fetchone()]
        for account in rows:
        # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
#                print (account)            
                session['loggedin'] = True
                session['password'] = account[2]
                session['username'] = account[2]

            # Redirect to home page
                return redirect('/')
            #return render_template('welcome.html', msg=msg)

            else:
            # Account doesnt exist or username/password incorrect
             msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/welcome', methods=['GET', 'POST', 'UPDATE'])
def welcome():
    if session.get('loggedin') is not None:
        return render_template('welcome.html',user=session['user'])  # render a template
    else:
        return redirect('/login')

## Session Token generation after login
@app.before_request
def before_request():
    g.user = None
    g.hostip = None
    if 'username' in session:
        session['user'] = session['username']

# Scenario pages 
@app.route('/scenario', methods=['GET', 'POST', 'UPDATE'])
def scenarioOne ():
    if session.get('loggedin') is not None:
        return render_template('scenarios.html')
    else:
        return redirect('/login')

# SSH Docker container IP
# This function generate or get IP Docker Container IP

@app.route('/connect', methods=['GET', 'POST', 'UPDATE'])
def ConnectInfo():
    if session.get('loggedin') is not None:
        ContainerName = None
        ContainerIP = None
        ip_add = None
        ContainerName = session['user']
        #client = docker.DockerClient(base_url='tcp://192.168.1.104:2375')
        client = docker.DockerClient()
        container = client.containers.get(session['user'])
        ContainerIP = container.attrs['NetworkSettings']['IPAddress']
        return ContainerIP
        g.hostip = ContainerIP
    else:
        return redirect('/login')
# Rendering page for docker container ssh 
@app.route('/ssh', methods=['GET', 'POST', 'UPDATE'])
def connectrout ():
    if session.get('loggedin') is not None:
        hostip = ConnectInfo()
        return render_template('ssh.html', hostip=hostip)
    else:
        return redirect('/login')

@app.route('/apache', methods=['GET'])
def apache ():
    if session.get('loggedin') is not None:
        #hostip = ConnectInfo()
        return render_template('apache.html')
    else:
        return redirect('/login')

# +++++++++++ I will Delete this code after sometime ++++++++
# @app.route('/mysql', methods=['GET'])                     +
# def mysql ():                                             +
#     if session.get('loggedin') is not None:               +
#         hostip = ConnectInfo()                            +
#         return render_template('mysql.html')              +
#     else:                                                 +
#         return redirect('/login')                         +    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

