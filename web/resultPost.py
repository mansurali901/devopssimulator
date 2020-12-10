
from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint,  jsonify
import docker
from docker import client
from flask_session import Session
import os
from ContainerCommit import containercommit
from dbconnection import connection # DB connection Module 

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)
# Blueprint declaration 
resultpost = Blueprint('resultpost',__name__)

# App Route
@resultpost.route('/resultpost', methods=['POST', 'GET'])
def index():
    if session.get('loggedin') is not None:
    # Initializing DB connection and DB Cursor 
    # Conn is cursor and c is DB connection     
        
        c, conn = connection()    
        Task = request.args.get('task', None)
        Username = request.args.get('user', None)
        Status = request.args.get('status', None)
        Data=[Task, Username, Status]
        # SQL query for posting Data for result
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        c.executemany(g.sqlfrom, Data)
        conn.commit()          
    else:
        return redirect('/login')        
    return 'end'
