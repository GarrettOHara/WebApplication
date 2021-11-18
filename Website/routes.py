# -----------------------------------------------------------
# Route definitions for Web Application
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------
import urllib
import threading as thread
from . import db
from . import results_graph
from sqlalchemy import text
from .models import Answer, Choice, Question
from flask import Blueprint, render_template, request, flash, redirect, url_for, session


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
    question = session['qid']
    sql = text(
        """
        SELECT q.text as Question, c.text AS Choice, COUNT(c.choice_id) AS Responses
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

    th = thread.Thread(target=results_graph.graph_values,args=(choices,responses), daemon=True)
    th.start()
    # th.join()
    # results_graph.graph(choices, responses)
    # STORE CHOICE ROWS IN LIST AS DICTIONARY OBJECTS
    # for r in result.keys():
    #     print(r)

    return render_template("results.html")


@routes.route('share_poll', methods=['GET'])
def share_poll():
    qid = session['qid']
    print("SHARE POLL: "+str(qid))
    parameters = {"qid": qid}
    url = "localhost:5000/answer_poll?"
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
