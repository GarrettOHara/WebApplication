# -----------------------------------------------------------
# Route definitions for Web Application
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------
import urllib
import time
import socket as sock
import threading as thread

from sqlalchemy.sql.functions import user
from . import db
from . import results_graph
from sqlalchemy import text
from .models import Answer, Choice, Question
from flask import Blueprint, render_template, request, flash, redirect, url_for, session


routes = Blueprint("routes", __name__)


@routes.route('/')
def home():
    sql = text(
    """
    SELECT question_id,text FROM question LIMIT 5;
    """
    )
    result = db.engine.execute(sql)

    responses = []
    choices = []
    print("RESULTS:")
    for r in result:
        responses.append(r['question_id'])
        choices.append(r['text'])
    print(responses)
    print(choices)
    return render_template("home.html")

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print()
        username = request.form.get('username')
        password = request.form.get('password')

        print(username)
        print(password)

        #if len(username) < 1 or len(password) < 1:
            #flash("Username or password entered is too short!", category="error")
        
    elif request.method == 'GET':
        print()
        sql = text(
            """
            SELECT COUNT(*)
            FROM addmin
            WHERE {}=username and {}=password;
            """
        )
        data = db.engine.execute(sql).fetchall()

        if 0 in data:
            flash("Error: Invalid login", category="error")
            return render_template("admin.html")
        
        session['admin'] = True

        return render_template("history.html")
    
    return render_template("admin.html")


@routes.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        #options = []
        #while(request.form.get('option') != None):
        #options.append(request.form.get('option'))

        options = request.form.getlist('option')

        print(len(options))

        #print("Question: {} \nOption: {}\nOption: {}".format(
            #question, option0, option1))

        error_control = 0

        if len(question) < 1:
            flash("Your question is too short!", category="error")
            error_control = 1
        
        for optn in options:
            if len(optn) < 1:
                flash("Please enter text for option", category="error")
                error_control = 1

        if error_control == 0:
            # CREATE AND WRITE POLL TO DATABASE
            poll = Question(text=question)
            db.session.add(poll)
            db.session.flush()

            # CREATE AND WRITE OPTIONS AND INITIAL
            # ANSWERS TO THE DATABASE
            op = 'A'
            for option in options:
                choice = Choice(question_id=poll.question_id,choice=op,text=option)
                op = chr(ord(op)+1)
                db.session.add(choice)
                db.session.flush()
                print(choice.choice_id)
                answer = Answer(choice_id=choice.choice_id,question_id=poll.question_id)
                db.session.add(answer)

            session['qid'] = poll.question_id

            db.session.commit()

            flash("Poll Created", category="success")
            return redirect(url_for('routes.share_poll'))

    return render_template("create_poll.html")


@routes.route('results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        question = session['qid']
        sql = text(
            """
            SELECT q.text as Question, c.text AS Choice, COUNT(c.choice_id)-1 AS Responses
            FROM question AS q, choice AS c, answer as a
            WHERE a.question_id = q.question_id and a.choice_id = c.choice_id and q.question_id = {}
            GROUP BY a.choice_id;
            """.format(question)
        )
        result = db.engine.execute(sql)

        responses = []
        choices = []
        question = ""
        print("RESULTS:")
        for r in result:
            responses.append(r['Responses'])
            choices.append(r['Choice'])

        # ORIGINAL GRAPHING METHOD
        th = thread.Thread(target=results_graph.graph_values,args=(choices,responses), daemon=True)
        th.start()
        time.sleep(1)

        return render_template("results.html")
        
    return render_template("results.html")

@routes.route('share_poll', methods=['GET'])
def share_poll():
    qid = session['qid']
    print("SHARE POLL: "+str(qid))
    parameters = {"qid": qid}
    
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    socket = s.getsockname()[0]
    s.close()
    url = "http://{}:5000/answer_poll?".format(socket)
    share = url+urllib.parse.urlencode(parameters)
    print(share)
    return render_template("share_poll.html", share=share)


@routes.route('/history', methods=['GET'])
def view_history():

    if request.method == 'GET':
        sql = text(
            """
            SELECT *,COUNT(*) as Repsonses
            FROM answer, question
            WHERE answer.question_id = question.question_id
            GROUP BY answer.question_id 
            ORDER BY Repsonses DESC;
            """
        )
        print(sql)
        data = db.engine.execute(sql).fetchall()

    return render_template("history.html", data=data)


@routes.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("search_polls.html")


@routes.route('/answer_poll', methods=['GET', 'POST'])
def answer_poll():
    # POST REQUEST
    if request.method == "POST":
        print("POST OF ANSWER")

        # GET ALL ANSWERS
        form = request.form.getlist('keys')

        # USER MUST ANSWER QUESTION, RE-RENDER TEMPLATE
        if len(form) == 0:
            flash("Please answer the question.", category="error")
            return render_template("answer_poll.html",question=session['qid'],data=session['question_object'])

        else:
            # CREATE AN ANSWER OBJECT FOR EACH CHOICE THE USER SELECTED
            for key in form:
                dic = session['question_object'][key]
                print(dic)
                choice = dic['choice_id']
                question = dic['question_id']
                answer = Answer(choice_id=choice,question_id=question)
                db.session.add(answer)

            # STORE QUESTION ID FOR RESULTS QUERY
            session['qid'] = question

            # WRITE ANSWERS TO DATABASE
            db.session.commit()

            # DISPLAY SUCCESSFUL WRITE TO USER
            flash("Response Recorded", category="success")
            return redirect(url_for('routes.results'))

    # GET REQUEST
    else:
        qid = request.args.get("qid")
        sql = text("SELECT * FROM question, choice WHERE question.question_id={} AND choice.question_id={}".format(qid,qid))
        result = db.engine.execute(sql)

        # STORE CHOICE ROWS IN LIST AS DICTIONARY OBJECTS
        dic = {}
        for r in result:
            dic[r['choice']] = dict(r.items())
        print(dic)

        # STORE DICTIONARY OF ROWS IN SESSION
        session['question_object'] = dic

        # GET QUESTION
        sql = text("SELECT text FROM question WHERE question_id={} LIMIT 1".format(qid))
        result = db.engine.execute(sql)
        for r in result:
            question=r[0]
        session['question'] = question

        return render_template("answer_poll.html",question=question,data=dic)
    

@routes.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404