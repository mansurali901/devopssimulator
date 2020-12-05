# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, g
import docker
from docker import client
from flask_session import Session
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
# Blueprints import here 
from ContainerCommit import containercommit
from containerCreate import containercreate


#import mysql.connector


# create the application object
app = Flask(__name__)
app.secret_key = "10pearls"  

app.register_blueprint(containercommit)
app.register_blueprint(containercreate)
# use decorators to link the function to a url
# Enter your database connection details below
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Welcome@1'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html',user=session['user'])  # render a template

@app.before_request
def before_request():
    g.user = None
    g.hostip = None
    if 'username' in session:
        session['user'] = session['username']


@app.route('/scenario')
def scenarioOne ():
    return render_template('scenarios.html')

@app.route('/Connect')
def ConnectInfo():
    ContainerName = None
    ContainerIP = None
    ip_add = None
    ContainerName = session['user']
    client = docker.DockerClient()
    container = client.containers.get(session['user'])
    ContainerIP = container.attrs['NetworkSettings']['IPAddress']
    return ContainerIP
    g.hostip = ContainerIP

@app.route('/ssh')
def connectrout ():
    hostip = ConnectInfo()
    #return hostip
    return render_template('ssh.html', hostip=hostip)

@app.route('/push')
def dockerPush():
    return "Welcome to docker Push page"

@app.route('/login', methods=['GET', 'POST'])
def index():
    msg = ''
    error = None
    user = None
#    mysql = ''
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

