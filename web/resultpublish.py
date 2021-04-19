import MySQLdb 
from flask import Flask, render_template 
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
publisher = Blueprint('publisher', __name__)

@publisher.route('/publisher', methods=['GET', 'POST', 'UPDATE'])

def example(): 
    
    conn = MySQLdb.connect("127.0.0.1","root","Welcome@1","pythonlogin" ) 
    cursor = conn.cursor() 
    cursor.execute("select * from results") 
    data = cursor.fetchall() #data from database 
    return render_template("example.html", value=data) 
