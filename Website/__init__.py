# -----------------------------------------------------------
# Defining global objects
#
# 2021  Garrett O'Hara, Nick Kokenis
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
# -----------------------------------------------------------

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()

# Testing the connection to the database
def connection():
    print("DATABASE CONNECTED, SHOWING TABLES:")
    sql = text("SHOW TABLES")
    result = db.engine.execute(sql)
    names = [row[0] for row in result]
    print(names)

def database_url():
    db_user = os.environ["CLOUD_SQL_USERNAME"]
    db_pass = os.environ["CLOUD_SQL_PASSWORD"]
    db_name = os.environ["CLOUD_SQL_DATABASE_NAME"]

    # DATABASE-URL: dialect+driver://username:password@host:port/database
    # DOCS: https://docs.sqlalchemy.org/en/14/core/engines.html
    database_url = "mysql+pymysql://{}:{}@localhost/{}".format(db_user, db_pass, db_name)
    
    return database_url

def create_app():
    app = Flask(__name__,template_folder='../Templates/')
    app.config['SECRET_KEY']="development secret key"
    app.config["STATIC_FOLDER"]="static"
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import routes

    app.before_first_request(connection)

    app.register_blueprint(routes,url_prefix='/')

    from .models import Question, Answer, Choice 

    create_database(app=app)
     
    return app

def create_database(app):
    db.create_all(app=app)