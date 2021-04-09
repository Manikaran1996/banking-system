from flask import request, render_template, redirect, url_for, session
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
    # TODO: check if user does not exist
    user = OnlineUser.query.filter(OnlineUser.user_name == username).first()
    if user is not None:
        password_in_db = user.password
        if bcrypt.check_password_hash(password_in_db, password):
            login_user(user)
            session['privilege_level'] = user.privilege_level
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
@app.route("/register-employee")
def register_employee():
    if session["privilege_level"] < 7:
        return redirect(url_for("transactions"))
    return render_template("create-employee.html")


@login_required
@app.route("/submit-emp-registration", methods=["POST"])
def add_emp_to_db():
    emp_name = request.form.get('employee_name')
    emp_id = request.form.get('emp_id')
    designation = request.form.get('designation')
    username = request.form.get('username')
    password = request.form.get('password')
    privilege_level = request.form.get('privilege_level')
    emp = Employee(emp_id=emp_id, emp_name=emp_name, designation=designation)
    online_user = OnlineUser(user_name=username, password=bcrypt.generate_password_hash(password),
                             employee_id=emp_id, privilege_level=privilege_level)
    db.session.add(emp)
    db.session.commit()
    db.session.add(online_user)
    db.session.commit()
    print("Successfully registered")
    return redirect(url_for("transactions"))


@login_required
@app.route("/transactions", methods=["GET"])
def transactions():
    return render_template("transaction-details.html")


@login_manager.user_loader
def load_user(_id):
    return OnlineUser.query.get(int(_id))
