from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

#app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '03911F29DB3EB9FC9E08DE88BE73'
secretKey = open('/run/secrets/app_secret_key', 'r').read().strip()
app.secret_key = secretKey
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.init_app(app)
migrate = Migrate(app, db)

from app import models
db.create_all()
db.session.commit()

from app import routes
