from app import db


class Bank(db.Model):
    branch_name = db.Column(db.String, nullable=False, primary_key=True)
    branch_code = db.Column(db.String, nullable=False)
    branch_address = db.Column(db.String, nullable=False)
