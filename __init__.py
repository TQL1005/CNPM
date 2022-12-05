from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:123456@localhost/airdb?charset=utf8mb4'

db = SQLAlchemy(app=app)

login = LoginManager(app=app)