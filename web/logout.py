from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint
import docker
from docker import client
from flask_session import Session
import requests

logout = Blueprint('logout', __name__)

@logout.route('/logout', methods=['GET', 'POST', 'UPDATE'])
def index():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return "Successfully log out from System"
    return redirect('/login')


