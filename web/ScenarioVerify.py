from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests

containercreate = Blueprint('containercreate', __name__)

@containercreate.route('/scene1')
def index():
    client = docker.from_env()
    ContainerName = session['user']