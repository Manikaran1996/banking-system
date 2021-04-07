from app import db


class AccountHolder(db.Model):
    account_number = db.Column(db.String, nullable=False, primary_key=True)
    gender = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    email_id = db.Column(db.String)
