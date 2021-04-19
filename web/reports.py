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
results = Blueprint('results', __name__)

@results.route('/results', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
     # Initializing DB connection and DB Cursor 
        # Conn is cursor and c is DB connection     
        # c, conn = connection()    
        # client = docker.from_env()
        # ContainerName = session['user']

        # Gloabal Veriables for different operations in module
        g.csID = session['user']
        # stage = session['stage'] 
        
        c, conn = connection()  
        g.sqlfrom = "insert into results (taskName, correct, wrong, total, username, percentage) values (%s, %s, %s, %s, %s, %s)"
        #g.update = "update results set percentage=("select * from("select r.correct * 100 / r.total from results r where taskName=%s", (bytaks,)))tbltmp) "where taskName=%s" (bytaks,));
        c.execute("select taskName from tasks")
        TasksNames = c.fetchall()

        for bytask in TasksNames:
            c.execute("select count(*) from scenarios where casenum=%s && username=%s", (bytask, g.csID))
            questionCount = c.fetchall()
            c.execute("select count(*) from scenarios where validation='true' && casenum=%s && username=%s", (bytask, g.csID,))
            correct = c.fetchall()
            c.execute("select count(*) from scenarios where validation='false' && casenum=%s && username=%s", (bytask, g.csID,))
            wrong = c.fetchall()
            c.execute("select total / correct * 100 from results where taskName=%s", (bytask,))
            deeppercentage = c.fetchall()
            print(bytask)
            print(deeppercentage)

            percentage = '100'
            Data = [(bytask, correct, wrong, questionCount, g.csID, percentage)]
            c.executemany(g.sqlfrom, Data)
            conn.commit() 
            
        c.close()
        return 'result added'
    else:
        return redirect('/login')
        
