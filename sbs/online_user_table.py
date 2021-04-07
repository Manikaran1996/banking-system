from app import db


class OnlineUser(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    account_number = db.Column(db.String, db.ForeignKey('account_holder.account_number'), unique=True)
    employee_id = db.Column(db.String, db.ForeignKey('employee.emp_id'))
    password = db.Column(db.String, nullable=False)



