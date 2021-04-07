from flask import request, render_template, redirect, url_for
from flask_login import login_required, login_user
from sbs.user import User
from sbs.online_user_table import OnlineUser
from sbs.employee_table import Employee
from sbs.account_holder_table import AccountHolder
from app import db, app, bcrypt, login_manager


@app.before_first_request
def create_tables():
    db.create_all()


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


@app.route("/register")
def register():
    return render_template("sign-up.html")


@app.route("/register-user", methods=["POST"])
def register_user():
    print(request.form)
    user_name = request.form.get('username')
    password = request.form.get('password')
    hashed_password = bcrypt.generate_password_hash(password)
    account_num = request.form.get('account_num')
    online_user = OnlineUser(user_name=user_name, password=hashed_password, account_number=account_num)
    db.session.add(online_user)
    db.session.commit()
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
