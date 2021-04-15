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
mysqltask = Blueprint('mysqltask', __name__)

@mysqltask.route('/mysql', methods=['GET', 'POST', 'UPDATE'])
def index():
    if session.get('loggedin') is not None:
        #hostip = ConnectInfo()
        return render_template('mysql.html')
    else:
        return redirect('/login')
        
# def ConnectInfo():
#     if session.get('loggedin') is not None:
#      # Initializing DB connection and DB Cursor 
#         # Conn is cursor and c is DB connection     
#         c, conn = connection()    
#         client = docker.from_env()
#         ContainerName = session['user']
#         # Gloabal Veriables for different operations in module
#         g.csID = session['user']

#         # SQL query for posting Data for result
#         g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
#         command = client.containers.get(g.csID)        
        
#         ################### Deprecated Not deleting for reason #######################
#         #g.scName = 'mysql'
#         #g.Task = ['server', 'pip','engine','dbnam','access','fpt']
#         #g.comContainer = ['dpkg -l mysql-server', 'netstat -ntlap |grep :3306 |grep mysql', 'curl -i web1.10pearls.com', 'ls -la /usr/share/doc/html/', 'curl -i --insecure https://web1.10pearls.com']
#         ##############################################################################

#         # Check if account exists using MySQL
    #     c, conn = connection()  
    #     c.execute("select * from conditions where server='mysql'")
    #     records = c.fetchall()
    #     for data in records:
    #         # Setup verification
    #         verifier = command.exec_run(g.data[2])
    #         # Converting docker exec Object to String 
    #         list_string = str(verifier)
    #         findbycode = list_string.find(data[4])
    #         if findbycode > 0:
    #             print('Condition validated')
    #             Data = [(g.data[3], "true", g.csID, g.data[1])]
    #             c.executemany(g.sqlfrom, Data)
    #             conn.commit()
    #         else:
    #             print('Not Installed')
    #             Data = [(g.data[3], "false", g.csID, g.data[1])]
    #             c.executemany(g.sqlfrom, Data)
    #             conn.commit()
    # else:
    #     return redirect('/login')
        
