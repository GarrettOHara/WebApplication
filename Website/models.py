# -----------------------------------------------------------
# MySQL ORM
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------

# Imports the database from __init__ scoped_session(...)
from . import db
from sqlalchemy.sql import func

class Question(db.Model):
    __tablename__='question'
    question_id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(280))
    live = db.Column(db.Boolean, unique=False, default=True)
    time_stamp = db.Column(db.DateTime(timezone = True), default=func.now())

class Choice(db.Model):
    __tablename__='choice'
    choice_id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    choice = db.Column(db.String(1))
    text = db.Column(db.String(280))


class Answer(db.Model):
    __tablename__='answer'
    answer_id = db.Column(db.Integer, primary_key = True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.choice_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    time_stamp = db.Column(db.DateTime(timezone = True), default=func.now())

    # SQL ALCHEMY ONLY | 1 TO MANY RELATIONSHIP
    choices = db.relationship('Choice')