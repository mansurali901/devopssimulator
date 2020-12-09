from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import os
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
from ContainerCommit import containercommit
import mysql.connector

# create the application object
app = Flask(__name__)
app.secret_key = "10pearls" 

# Application configuration file
app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

# Enter your database connection details below
app.config['MYSQL_HOST'] = app.config.get("MYSQL_HOST_IP")
app.config['MYSQL_USER'] = app.config.get("MYSQL_USER")   
app.config['MYSQL_PASSWORD'] = app.config.get("MYSQL_PASS")
app.config['MYSQL_DB'] = app.config.get("AUTHDB")

# Intialize MySQL
mydb = mysql.connector.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'], passwd=app.config['MYSQL_PASSWORD'], database=app.config['MYSQL_DB'])   

containerverify = Blueprint('containerverify', __name__)
@containerverify.route('/verify', methods=['GET', 'POST', 'UPDATE'])
def apache2():
    if session.get('loggedin') is not None:
        client = docker.from_env()
        ContainerName = session['user']
        g.csID = session['user']
        g.scName = 'apache'
        g.Task = 'server'
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        command = client.containers.get(g.csID)
        firstString = []
        apache2 = command.exec_run("dpkg -l apache2")
        list_string = str(apache2)
        final = list_string.find('code=0')
        if final > 0:
            print('Package is installed')
            mycursor = mydb.cursor()
            Data = [(g.scName, "true", g.csID, g.Task)]
            mycursor.executemany(g.sqlfrom, Data)
            mydb.commit()            
        else:
            print('Not Installed')
            mycursor = mydb.cursor()
            Data = [(g.scName,'false', g.csID)]
            #sqlfrom = "insert into scenarios (casenum, validation, username) values (%s, %s, %s)"
            mycursor.executemany(g.sqlfrom, Data)
            mydb.commit()
        return 'end'

    else:
        return redirect('/login')



