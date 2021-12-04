# -----------------------------------------------------------
# Route definitions for Web Application
#
# 2021  Garrett O'Hara, Nick Kokenis
# email garrettohara2018@gmail.com
#       nkokenis3597@sdsu.edu
# -----------------------------------------------------------

from functools import reduce
from re import S
import time
import urllib
import socket as sock
import threading as thread
from . import db
from os import error
from . import results_graph
from sqlalchemy import text
from sqlalchemy.sql.functions import user
from .models import Answer, Choice, Question
from flask.templating import render_template_string
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
    for r in result:
        responses.append(r['question_id'])
        choices.append(r['text'])
    return render_template("home.html")

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None or len(username) < 1 or len(password) < 1:
            flash("Error: Please enter a username and password.", category="error")
            return render_template("admin.html")
        sql = text(
            """
            SELECT COUNT(*)
            FROM admin
            WHERE '{}'=username and '{}'=password;
            """.format(username,password)
        )
        data = db.engine.execute(sql).fetchall()

        if data[0][0] == 0:
            flash("Error: Invalid login.", category="error")
            return render_template("admin.html")
        else:
            session['admin'] = True
            return redirect(url_for('routes.manage_polls'))
    else:
        return render_template("admin.html")

@routes.route('/manage_polls', methods=['GET','POST'])
def manage_polls():
    if request.method == "POST":
        poll_id = request.form.get('option')
        session['pollid'] = poll_id
        return redirect(url_for('routes.poll_info'))
    else:
        return render_template("manage_polls.html")

@routes.route('/poll_info', methods=['GET','POST'])
def poll_info():
    poll_id = session.get('pollid', None)
    if request.method == "GET":
        sql = text("SELECT * FROM question WHERE question.question_id={}".format(poll_id))
        result = db.engine.execute(sql).fetchall()
        return render_template("poll_info.html", data=result)
    elif request.method == "POST":
        if request.form.get('delete'):
            sql = text(
                """
                DELETE FROM question WHERE question_id={};
                """.format(poll_id)
            )
            db.engine.execute(sql)
            sql = text(
                """
                DELETE FROM choice WHERE question_id={};
                """.format(poll_id)
            )
            db.engine.execute(sql)
            sql = text(
                """
                DELETE FROM answer WHERE question_id={};
                """.format(poll_id)
            )
            flash("Success: Poll deleted.", category="success")
        elif request.form.get('edit'):
            ans = request.form.get('option')

            if ans is None or len(ans) < 1:
                return redirect(url_for('routes.manage_polls'))

            sql = text(
                """
                UPDATE question SET question.text='{}' WHERE question.question_id={};
                """.format(ans,poll_id)
            )
            db.engine.execute(sql)
            flash("Success: Poll updated.")
        return redirect(url_for('routes.manage_polls'))

@routes.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        options = request.form.getlist('option')
        error_control = 0
        if len(question) < 1:
            flash("Error: Please enter a question.", category="error")
            error_control = 1
        for optn in options:
            if len(optn) < 1:
                flash("Error: Please enter at least two (2) options.", category="error")
                error_control = 1

        if error_control == 0:
            poll = Question(text=question)
            db.session.add(poll)
            db.session.flush()
            op = 'A'
            for option in options:
                choice = Choice(question_id=poll.question_id,choice=op,text=option)
                op = chr(ord(op)+1)
                db.session.add(choice)
                db.session.flush()
                answer = Answer(choice_id=choice.choice_id,question_id=poll.question_id)
                db.session.add(answer)
            session['qid'] = poll.question_id
            db.session.commit()
            flash("Success: Poll created.", category="success")
            return redirect(url_for('routes.share_poll'))

    return render_template("create_poll.html")

@routes.route('/results', methods=['GET', 'POST'])
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
        for r in result:
            responses.append(r['Responses'])
            choices.append(r['Choice'])
        
        th = thread.Thread(target=results_graph.graph_values,args=(choices,responses), daemon=True)
        th.start()
        time.sleep(1)

        return render_template("results.html")
        
    return render_template("results.html")

@routes.route('/share_poll', methods=['GET'])
def share_poll():
    qid = session['qid']
    parameters = {"qid": qid}
    
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    socket = s.getsockname()[0]
    s.close()
    url = "http://{}:5000/answer_poll?".format(socket)
    share = url+urllib.parse.urlencode(parameters)
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
        data = db.engine.execute(sql).fetchall()
        return render_template("history.html", data=data)

@routes.route('/answer_poll', methods=['GET', 'POST'])
def answer_poll():
    if request.method == "POST":
        form = request.form.getlist('keys')
        if len(form) == 0:
            flash("Error: Please submit an answer.", category="error")
            return render_template("answer_poll.html",question=session['qid'],data=session['question_object'])
        else:
            for key in form:
                dic = session['question_object'][key]
                choice = dic['choice_id']
                question = dic['question_id']
                answer = Answer(choice_id=choice,question_id=question)
                db.session.add(answer)
            session['qid'] = question
            db.session.commit()
            flash("Success: Response recorded.", category="success")
            return redirect(url_for('routes.results'))
    else:
        qid = request.args.get("qid")
        sql = text("SELECT * FROM question, choice WHERE question.question_id={} AND choice.question_id={}".format(qid,qid))
        result = db.engine.execute(sql)
        dic = {}
        for r in result:
            dic[r['choice']] = dict(r.items())
        session['question_object'] = dic
        sql = text("SELECT text FROM question WHERE question_id={} LIMIT 1".format(qid))
        result = db.engine.execute(sql)
        for r in result:
            question=r[0]
        session['question'] = question

        return render_template("answer_poll.html",question=question,data=dic)

@routes.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404