"""empty message

Revision ID: 1c5ee1ec8d80
Revises: ffb063c7d91e
Create Date: 2021-04-11 11:23:51.097336

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1c5ee1ec8d80'
down_revision = 'ffb063c7d91e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('account_number', table_name='online_user')
    # op.drop_index('employee_id', table_name='online_user')
    # op.drop_index('user_name', table_name='online_user')
    # op.drop_table('online_user')
    # op.drop_table('employee')
    # op.drop_index('branch_name', table_name='bank')
    op.drop_table('account_holder')
    op.drop_table('bank')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_holder',
    sa.Column('account_number', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('gender', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('phone', mysql.VARCHAR(length=13), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('email_id', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('branch_code', mysql.VARCHAR(length=30), nullable=False),
    sa.ForeignKeyConstraint(['branch_code'], ['bank.branch_code'], name='account_holder_ibfk_1'),
    sa.PrimaryKeyConstraint('account_number'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('bank',
    sa.Column('branch_name', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('branch_code', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('branch_address', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('branch_code'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('branch_name', 'bank', ['branch_name'], unique=True)
    op.create_table('employee',
    sa.Column('emp_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('emp_name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('designation', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('emp_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('online_user',
    sa.Column('_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_name', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('account_number', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('employee_id', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('privilege_level', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['account_number'], ['account_holder.account_number'], name='online_user_ibfk_1'),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.emp_id'], name='online_user_ibfk_2'),
    sa.PrimaryKeyConstraint('_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('user_name', 'online_user', ['user_name'], unique=True)
    op.create_index('employee_id', 'online_user', ['employee_id'], unique=True)
    op.create_index('account_number', 'online_user', ['account_number'], unique=True)
    # ### end Alembic commands ###