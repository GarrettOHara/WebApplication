# -----------------------------------------------------------
# Route definitions for Web Application
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------

import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Answer, Choice, Question
from . import db

routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    return render_template("home.html")

@routes.route('/create_poll', methods=['GET','POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        option0 = request.form.get('option0')
        option1 = request.form.get('option1')

        print("Question: {} \nOption: {}\nOption: {}".format(question,option0,option1))

        if len(question) < 1:
            flash("Your question is too short!", category="error")
        elif len(option0) < 1 or len(option1) < 1:
            flash("Please enter text for option", category="error")
        else:
            # IF WE WANT POLL PREVIEW WE NEED TO MOVE THIS
            # THERE THIS CREATES IT RIGHT AWAT
            # new_poll = Question(text=question)
            # db.session.add(new_poll)
            # db.session.commit()
            flash("Poll Created", category="success")
            return redirect(url_for('routes.share_poll'))


    return render_template("create_poll.html")

@routes.route('poll_review', methods=['GET','POST'])
def review_poll():
    return render_template("poll_review.html")

@routes.route('share_poll', methods=['GET'])
def share_poll():
    return render_template("share_poll.html")

@routes.route('/history', methods=['GET','POST'])
def view_history():
    return render_template("history.html")

@routes.route('/search', methods=['GET','POST'])
def search():
    return render_template("search_polls.html")

@routes.route('/answer_poll', methods=['GET','POST'])
def anser_poll():
    return render_template("poll.html")