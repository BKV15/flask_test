from flask import Flask
from .extensions import mongo
import os
from flask_login import LoginManager

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6ab8eca495edfc8b82706e937cb3cdf82a4392af14705543c9b06e8118342f71'
    app.config['MONGODB_SETTINGS'] = {
    'db': 'test_db',
    'host': os.getenv('MONGODB_HOST', 'localhost:27017'),
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