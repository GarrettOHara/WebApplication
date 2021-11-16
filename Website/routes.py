# -----------------------------------------------------------
# Route definitions for Web Application
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------

import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Answer, Choice, Question
from . import db
import urllib
from sqlalchemy import text
from flask import jsonify

routes = Blueprint("routes", __name__)


@routes.route('/')
def home():
    return render_template("home.html")


@routes.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        option0 = request.form.get('option0')
        option1 = request.form.get('option1')
        options = [option0,option1]

        print("Question: {} \nOption: {}\nOption: {}".format(
            question, option0, option1))

        if len(question) < 1:
            flash("Your question is too short!", category="error")
        elif len(option0) < 1 or len(option1) < 1:
            flash("Please enter text for option", category="error")
        else:
            # IF WE WANT POLL PREVIEW WE NEED TO MOVE THIS
            # THERE THIS CREATES IT RIGHT AWAT
            poll = Question(text=question)
            db.session.add(poll)
            db.session.flush()

            op = 'A'
            for option in options:
                choice = Choice(question_id=poll.question_id,choice=op,text=option)
                op = chr(ord(op)+1)
                db.session.add(choice)

            session['qid'] = poll.question_id

            db.session.commit()

            flash("Poll Created", category="success")
            return redirect(url_for('routes.share_poll'))

    return render_template("create_poll.html")


@routes.route('results', methods=['GET', 'POST'])
def results():
    return render_template("results.html")


@routes.route('share_poll', methods=['GET'])
def share_poll():
    qid = session['qid']
    print("SHARE POLL: "+str(qid))
    parameters = {"qid": qid}
    url = "http://localhost:5000/answer_poll?"
    share = url+urllib.parse.urlencode(parameters)
    print(share)
    return render_template("share_poll.html", share=share)


@routes.route('/history', methods=['GET', 'POST'])
def view_history():
    return render_template("history.html")


@routes.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("search_polls.html")


@routes.route('/answer_poll', methods=['GET', 'POST'])
def anser_poll():
    if request.method == "GET":
        qid = request.args.get("qid")
        sql = text("SELECT * FROM question, choice WHERE question.question_id={} AND choice.question_id={}".format(qid,qid))
        result = db.engine.execute(sql)

        # STORE CHOICE ROWS IN LIST AS DICTIONARY OBJECTS
        dics = []
        for r in result:
            dics.append(dict(r.items())) # convert to dict keyed by column names
        print(dics)

        # GET QUESTION
        sql = text("SELECT text FROM question WHERE question_id={}".format(qid))
        result = db.engine.execute(sql)
        question = ""
        for r in result:
            question=r[0]
        print(question)
        return render_template("answer_poll.html",question=question,data=dics)
    
    if request.method == "POST":
        print("POST OF ANSWER")
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print(key+":"+value)
        
        flash("Response Recorded", category="success")
        return redirect(url_for('routes.results'))
        
    


@routes.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
