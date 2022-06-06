from flask import Flask
from .extensions import mongo
import os
from flask_login import LoginManager

MONGODB_URI = os.environ['MONGODB_URI']
SECRET_KEY = os.environ['SECRET_KEY']

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MONGODB_SETTINGS'] = {
    'db': 'test_db',
    'host': MONGODB_URI,
    }

    mongo.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views , url_prefix='/')
    app.register_blueprint(auth , url_prefix='/')

    from .models import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.objects(id=id).first()

    return app