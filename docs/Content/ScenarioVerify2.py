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

containerverify2 = Blueprint('containerverify2', __name__)

@containerverify2.route('/verify2', methods=['GET', 'POST', 'UPDATE'])
######### POST Function will bring up in next release
# def PostData(user=None, task=None, status=None):
    
#     command = "'http://127.0.0.1:5000/resultpost?task=' + setup + '&user=' + user + '&' status= + status"
#     os.system(command)

def apache22():
    if session.get('loggedin') is not None:
        # Initializing DB connection and DB Cursor 
        # Conn is cursor and c is DB connection     
        c, conn = connection()    
        client = docker.from_env()
        ContainerName = session['user']
        # Gloabal Veriables for different operations in module
        g.csID = session['user']
        g.scName = 'apache'
        g.Task = ['dpkg', 'netstat','curl','ls','--insecure']
        g.comContainer = ['dpkg -l apache2', 'netstat -ntlap |grep :80 |grep apache', 'curl -i web1.10pearls.com', 'ls -la /usr/share/doc/html/', 'curl -i --insecure https://web1.10pearls.com']
        g.Conditions = ['code=0','0.0.0.0:80', '200', 'root']
        # SQL query for posting Data for result
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        command = client.containers.get(g.csID)

        for comm in g.comContainer:
            Execution = command.exec_run(comm)
            list_string_execution = str(Execution)
            ConditionLength = len(g.Conditions)
            instruction = None
            comm = instruction
        
            for stringFind in range(ConditionLength):
                stringLocate = list_string_execution.find(g.Conditions[stringFind])
                if stringLocate > 0:
                    counter = len(g.Task)
                    for increment in range(counter):
                        print('Debug : ' + instruction)
                        taskFind = g.instructions.find(g.Task[increment])
                        if taskFind > 0:
                            g.category = g.Task[increment]
                            Data = [(g.scName,'true', g.csID, g.Task[increment])]
                            c.executemany(g.sqlfrom, Data)
                            conn.commit()
                            #print('Setup is verfied !!')
                        else:
                            print('Task not Found ...!')

                    # Data Commit to DB with True condition 

                else:
                    # Data commit with condition failure
                    print('Fale condition !!')
                    Data = [(g.scName,'false', g.csID, 'dump')]
                    c.executemany(g.sqlfrom, Data)
                    conn.commit()
        return 'end'
    else:
        return redirect('/login')