from app import db


class Employee(db.Model):
    emp_id = db.Column(db.String, primary_key=True)
    emp_name = db.Column(db.String)
    privilege_level = db.Column(db.Integer)
