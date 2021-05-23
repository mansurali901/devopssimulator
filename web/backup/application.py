# from flask import Flask, render_template, jsonify, request,redirect,flash,session
# from models import *
# folder_name="static"

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:yourpasswrodhere @localhost:5432/OnlineQuiz"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = b'hkahs3720/' # use a random string
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# db.init_app(app)

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
linux = Blueprint('linux', __name__)

@linux.route('/linux', methods=['GET', 'POST', 'UPDATE'])
#to change color of question buttons and disable 
def setStatus(qlist):
    qAttempt=[]
    strval=session['result'].strip()
    ans=strval.split(',')
    for i in range(int(len(ans)/2)):
        qAttempt.append(int(ans[2*i]))  
    
    for rw in qlist:
        if rw.qid in qAttempt:
            rw.bcol='green'   # set color
            rw.status='disabled' # disable

@app.route("/linuxquiz")
def index():
    session['result']=""
    subList=questions.query.with_entities(questions.subject).distinct()
    return render_template("linuxquiz.html",subList=subList)  

@app.route('/quiz', methods=["POST"])
def quiz(): 
    subject= request.form.get('sub')
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(subject=subject).first()
    return render_template("dashboard.html",questList=questList, quest=quest) 
    
    
@app.route("/showQuest/<string:subject>,<int:qid>")
def showQuest(subject,qid):
    questList=questions.query.filter_by(subject=subject).all()
    quest=questions.query.filter_by(qid=qid).first()
    setStatus(questList)
    return render_template("dashboard.html",questList=questList, quest=quest)  
    
@app.route('/saveAns',methods=["POST"]) 
def saveAns():
    qid=request.form.get('qid')
    ans=request.form.get('answer')
    sub=request.form.get('subject')
    #update the question id and its selected answer in session variable result
    res=session['result']
    res= res+qid+','+ans+','
    session['result']=res
    questList=questions.query.filter_by(subject=sub).all()
    setStatus(questList)
    quest=questions.query.filter_by(qid=qid).first()
    return render_template("dashboard.html",questList=questList, quest=quest)  
        
@app.route("/logout")
def logout():
    #calculate result
    count=0
    txt=""
    strval=session['result'].strip()
    #split result string by ','
    ans=strval.split(',')
    for i in range(int(len(ans)/2)):
        qd=ans[2*i] # get question id
        qn=ans[2*i+1]  # get the sorresponding answer
        tt=int(qd)
        quest=questions.query.filter_by(qid=tt).first()
        actans=quest.answer
        if actans==int(qn):#compare correct answer in questions table with answer chosen by user
            count=count+1 # increment counter
    txt=txt+'You have '+ str(count)+ ' correct questions out of '+ str(int(len(ans)/2))+ ' questions ' # set the result statement
    return render_template("result.html",txt=txt) 