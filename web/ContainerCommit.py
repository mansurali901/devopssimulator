# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests
import datetime
import os 

containercommit = Blueprint('containercommit', __name__)

@containercommit.route('/commit')
def index():

    containerSessionID = session['user']
    registryName = 'mansurali901'
    ImageName = registryName + '/' + containerSessionID
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%b%d")
    client = docker.from_env()
    container = client.containers.get(containerSessionID)
    print("Start Building your docker image...")
    container.commit(repository=containerSessionID, tag=timestamp)
    client.containers.get(containerSessionID) 
    container.stop()
    container.remove()
    return "Image has been commited"