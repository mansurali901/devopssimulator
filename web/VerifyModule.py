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
mysqlverify = Blueprint('mysqlverify', __name__)

@mysqlverify.route('/mysqlverify', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
     # Initializing DB connection and DB Cursor 
        # Conn is cursor and c is DB connection     
        c, conn = connection()    
        client = docker.from_env()
        ContainerName = session['user']
        # Gloabal Veriables for different operations in module
        g.csID = session['user']

        # SQL query for posting Data for result
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        command = client.containers.get(g.csID)        
        
        ################### Deprecated Not deleting for reason #######################
        #g.scName = 'mysql'
        #g.Task = ['server', 'pip','engine','dbnam','access','fpt']
        #g.comContainer = ['dpkg -l mysql-server', 'netstat -ntlap |grep :3306 |grep mysql', 'curl -i web1.10pearls.com', 'ls -la /usr/share/doc/html/', 'curl -i --insecure https://web1.10pearls.com']
        ##############################################################################

        # Check if account exists using MySQL
        c, conn = connection()  
        c.execute("select * from conditions where stage='mysql'")
        records = c.fetchall()
        #print(records)
        for data in records:
            #print(data)
            # Setup verification
            #print(data[1])
            verifier = command.exec_run(data[1])
            # Converting docker exec Object to String 
            list_string = str(verifier)
            print(list_string)
            findbycode = list_string.find(data[2])
            if findbycode > 0:
                print('Condition validated')
                Data = [(data[5], "true", g.csID, data[3])]
                c.executemany(g.sqlfrom, Data)
                conn.commit()
                #return redirect('/mysql')
            else:
                print('Not Installed')
                Data = [(data[5], "false", g.csID, data[3])]
                c.executemany(g.sqlfrom, Data)
                conn.commit()
                #return redirect('/mysql')
        return 'conditionvalidated'
    else:
        return redirect('/login')
        
