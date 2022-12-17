from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_admin import Admin
import cloudinary
from flask_babelex import Babel

app = Flask(__name__)
app.secret_key = 'asdsd34343545dfdfd55t4'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:%s@localhost/airdb?charset=utf8mb4' %quote('123456789')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)


admin = Admin(app=app, name='QUẢN LÝ MÁY BAY', template_mode='bootstrap4')