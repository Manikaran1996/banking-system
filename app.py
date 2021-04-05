from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_required, login_user
from user import User

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = "MySecureBankingApp"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("bankPassword")
    if username == "admin" and password == "admin":
        login_user(User(username, 1))
        return redirect(url_for('transactions'))
    print("Username and password does not match")
    return redirect(url_for('index'))


@login_required
@app.route("/transactions", methods=["GET"])
def transactions():
    return render_template("transaction-details.html")


@login_manager.user_loader
def load_user(_id):
    if _id == 1:
        return User('admin', 1)
    return None


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
