from flask import Flask

def create_app():
    app = Flask(__name__,template_folder='../Templates/')
    app.config['SECRET_KEY']="development secret key"

    from .routes import routes

    app.register_blueprint(routes,url_prefix='/')
     
    return app