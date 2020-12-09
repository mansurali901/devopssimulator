from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
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

containerverify = Blueprint('containerverify', __name__)
@containerverify.route('/verify', methods=['GET', 'POST', 'UPDATE'])
def apache2():
    if session.get('loggedin') is not None:
        # Initializing DB connection and DB Cursor 
        # Conn is cursor and c is DB connection     
        c, conn = connection()    
        client = docker.from_env()
        ContainerName = session['user']
        # Gloabal Veriables for different operations in module
        g.csID = session['user']
        g.scName = 'apache'
        g.Task = 'server'

        # SQL query for posting Data for result
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        command = client.containers.get(g.csID)
        # Package verification
        apache2 = command.exec_run("dpkg -l apache2")
        # Converting docker exec Object to String 
        list_string = str(apache2)
        final = list_string.find('code=0')
        if final > 0:
            print('Package is installed')
            Data = [(g.scName, "true", g.csID, g.Task)]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('Not Installed')
            Data = [(g.scName,'false', g.csID)]
            c.executemany(g.sqlfrom, Data)
            conn.commit()
        return 'end'
    else:
        return redirect('/login')