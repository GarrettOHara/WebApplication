# -----------------------------------------------------------
# DEPRICATED Legacy connect
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------

import os
import sqlalchemy
from Website import create_app

app = create_app()

def init_tcp_connection_engine():
    db_user = os.environ["CLOUD_SQL_USERNAME"]
    db_pass = os.environ["CLOUD_SQL_PASSWORD"]
    db_name = os.environ["CLOUD_SQL_DATABASE_NAME"]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host='127.0.0.1',  # 192.168.1.186',  # e.g. "127.0.0.1"
            port=3306,
            database=db_name,  # e.g. "production"
        ),
    )
    return pool


db = None


@app.before_first_request
def create_tables():
    global db
    db = init_tcp_connection_engine()
    print("database connected :)")
    # with db.connect() as conn:
    #     conn.execute(
    #         "CREATE TABLE IF NOT EXISTS votes "
    #         "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
    #         "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
    #     )
@app.before_request
def before_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def describe_schema():
    schema = []
    with db.connect() as conn:
        tmp = conn.execute("DESCRIBE test")
        for row in tmp:
            schema.append({
                'field': row[0],
                'Type': row[1],
                'Null': row[2],
                'Key': row[3],
                'Default': row[4],
                'Extra': row[5]
            })

    return {
        'schema': schema
    }


@app.route("/", methods=["GET"])
def home():
    res = describe_schema()
    return res# render_template('home.html')


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error.html'), 404

def run():
    print("Starting server...")
    app.debug = True
    app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000, threaded=True)
