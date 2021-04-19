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

@containerverify.route('/apacheCheck', methods=['GET', 'POST', 'UPDATE'])
######### POST Function will bring up in next release
# def PostData(user=None, task=None, status=None):
    
#     command = "'http://127.0.0.1:5000/resultpost?task=' + setup + '&user=' + user + '&' status= + status"
#     os.system(command)

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
        g.Task = ['server', 'portverify','alias','directory','ssl']
        g.comContainer = ['dpkg -l apache2', 'netstat -ntlap |grep :80 |grep apache', 'curl -i web1.10pearls.com', 'ls -la /usr/share/doc/html/', 'curl -i --insecure https://web1.10pearls.com']
        # SQL query for posting Data for result
        g.sqlfrom = "insert into scenarios (casenum, validation, username, task) values (%s, %s, %s, %s)"
        command = client.containers.get(g.csID)

        # Setup verification
        apache2 = command.exec_run(g.comContainer[0])
        PortVerify = command.exec_run(g.comContainer[1])
        Alias = command.exec_run(g.comContainer[2])
        Directory = command.exec_run(g.comContainer[3])
        SSL = command.exec_run(g.comContainer[4])

        # Converting docker exec Object to String 
        list_string = str(apache2)
        list_string_port = str(PortVerify)
        list_string_alias = str(Alias)
        list_string_directory = str(Directory)
        list_string_ssl = str(SSL)

        # Conditions setup variables
        final = list_string.find('code=0')
        port = list_string_port.find('0.0.0.0:80')
        alias = list_string_alias.find('200')
        directory = list_string_directory.find('root')
        ssl = list_string_ssl.find('200')
        if final > 0:
            print('Package is installed')
            Data = [(g.scName, "true", g.csID, g.Task[0])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('Not Installed')
            Data = [(g.scName,'false', g.csID,g.Task[0])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()
            
        if port > 0:
            print('Apache is running at 0.0.0.0:80')
            Data = [(g.scName, "true", g.csID, g.Task[1])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('Apache is not running at 0.0.0.0:80')
            Data = [(g.scName,'false', g.csID,g.Task[1])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()

        if alias > 0:
            print('Server is accessible via alias')
            Data = [(g.scName, "true", g.csID, g.Task[2])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('Server is not accessible via alias')
            Data = [(g.scName,'false', g.csID, g.Task[2])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()

        if directory > 0:
            print('Dicrectory is correctly Setup')
            print(Directory)
            Data = [(g.scName, "true", g.csID, g.Task[3])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('Dicrectory is not correctly Setup')
            print(Directory)
            Data = [(g.scName,'false', g.csID, g.Task[3])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()

        if ssl > 0:
            print('SSL is Setup correctly')
            print(SSL)
            Data = [(g.scName, "true", g.csID, g.Task[4])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()            
        else:
            print('SSL is not Setup correctly')
            print(SSL)
            Data = [(g.scName,'false', g.csID, g.Task[4])]
            c.executemany(g.sqlfrom, Data)
            conn.commit()
        return 'end'
    else:
        return redirect('/login')