from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banking.db"
app.secret_key = "MySecureBankingApp"

login_manager = LoginManager(app)
db: SQLAlchemy = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from routes import *

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
