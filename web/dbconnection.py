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

def dbCheck ():
    # Application configuration file
    app.config.from_pyfile(os.path.join("..", "conf/app.conf"), silent=False)

    # Enter your database connection details below
    app.config['MYSQL_HOST'] = app.config.get("MYSQL_HOST_IP")
    app.config['MYSQL_USER'] = app.config.get("MYSQL_USER")   
    app.config['MYSQL_PASSWORD'] = app.config.get("MYSQL_PASS")
    app.config['MYSQL_DB'] = app.config.get("AUTHDB")
    # Intialize MySQL
    mydb = mysql.connector.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'], passwd=app.config['MYSQL_PASSWORD'], database=app.config['MYSQL_DB'])   
    return 'DB Check'

