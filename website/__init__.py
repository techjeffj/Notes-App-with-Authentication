from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Database setup
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key_for_testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #path to the database
    db.init_app(app)


# import the views
    from .views import views
    from .auth import auth

# register the route blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

# import models to define the tables before creating the db
    from .models import User, Note

    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where should flask redirect us if we are not logged in
    login_manager.init_app(app) # tell loginManager which app we are using

    # this tell flask how we load a user
    @login_manager.user_loader #this decorator is telling flask to use this func to load user
    def load_user(id):
        return User.query.get(int(id)) # looks for the primary key. tells flask that we are using the User model and referencing by the userid

    return app

def create_database(app):
    # check if the database exists. If it doesn't, create it
    if not path.exists('website/' + DB_NAME): 
        db.create_all(app=app) # passes 'app' to tell alchemy which app to create the db for
        print('Created Database!')
