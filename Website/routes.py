from flask import Blueprint, render_template, request, flash

routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    return render_template("home.html")

@routes.route('/create_poll', methods=['GET','POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        option = request.form.get('option')
        print("Question: {} \n Option: {}".format(question,option))

        if len(question) < 10:
            flash("Your question is too short!", category="error")
        elif len(option) < 1:
            flash("Please enter text for option", category="error ")
        else:
            print("Add data to database")

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