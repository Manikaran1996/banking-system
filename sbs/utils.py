# from .account_holder_table import AccountHolder
import hashlib
import time
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import and_
from sqlalchemy.sql import func

from app import db_session
from sbs.models.tables import *

ACCOUNT_NUM_PREFIX = "SBS"


def get_last_account_num(branch_code):
    # account_num_row = AccountHolder.query\
    #    .with_entities(func.max(AccountHolder.account_number).label("max_account"))\
    #    .filter(AccountHolder.branch_code == branch_code)\
    #    .first()

    try:
        account_num_row = db_session.query(func.max(AccountHolder.account_number).label("max_account")) \
            .filter(AccountHolder.branch_code == branch_code) \
            .one()[0]
    except NoResultFound:
        account_num_row = None
    return account_num_row


def get_latest_account_num(branch_code):
    account_num_row = get_last_account_num(branch_code)
    if account_num_row is None:
        max_account_id = 1
    else:
        print(account_num_row)
        max_account_id = int(account_num_row[-8:]) + 1
    print(max_account_id)
    account_num = '{}{}{:0>8}'.format(ACCOUNT_NUM_PREFIX, branch_code, max_account_id)
    return account_num


def get_account_balance(account_number):
    credit = db_session.query(func.sum(Transaction.amount)) \
        .filter(and_(Transaction.account_number == account_number,
                     Transaction.transaction_type == Transaction.get_credit_type())) \
        .one()[0]

    debit = db_session.query(func.sum(Transaction.amount)) \
        .filter(and_(Transaction.account_number == account_number,
                     Transaction.transaction_type == Transaction.get_debit_type())) \
        .one()[0]

    return (0 if credit is None else credit) - (0 if debit is None else debit)


def get_transaction_id(account_number):
    return '{}{}'.format(hashlib.sha1(account_number.encode()).hexdigest()[:10], int(time.time()))


def transfer_amount_db(source_account: str, to_account: str, amount: float, description: str = None):
    balance = get_account_balance(source_account)
    if balance < amount:
        return False, "Transaction Failed! Insufficient funds."
    source_transaction_id = get_transaction_id(source_account)
    source_transaction = Transaction(transaction_id=source_transaction_id,
                                     transaction_time=datetime.now(),
                                     account_number=source_account,
                                     amount=amount,
                                     transaction_type=Transaction.get_debit_type(),
                                     details=description)
    receiver_transaction_id = get_transaction_id(to_account)
    receiver_transaction = Transaction(transaction_id=receiver_transaction_id,
                                       transaction_time=datetime.now(),
                                       account_number=to_account,
                                       amount=amount,
                                       transaction_type=Transaction.get_credit_type(),
                                       details=description)
    db_session.add(source_transaction)
    db_session.add(receiver_transaction)
    db_session.commit()
    return True, "Transaction Successful"


def deposit_money_db(source_account: str, amount: float, description: str = None):
    source_transaction_id = get_transaction_id(source_account)
    source_transaction = Transaction(transaction_id=source_transaction_id,
                                     transaction_time=datetime.now(),
                                     account_number=source_account,
                                     amount=amount,
                                     transaction_type=Transaction.get_credit_type(),
                                     details=description)
    db_session.add(source_transaction)
    db_session.commit()
    return True, "Transaction Successful"


def withdraw_money_db(source_account: str, amount: float, description: str = None):
    balance = get_account_balance(source_account)
    if balance < amount:
        return False, "Transaction Failed! Insufficient funds."
    source_transaction_id = get_transaction_id(source_account)
    source_transaction = Transaction(transaction_id=source_transaction_id,
                                     transaction_time=datetime.now(),
                                     account_number=source_account,
                                     amount=amount,
                                     transaction_type=Transaction.get_debit_type(),
                                     details=description)
    db_session.add(source_transaction)
    db_session.commit()
    return True, "Transaction Successful"
