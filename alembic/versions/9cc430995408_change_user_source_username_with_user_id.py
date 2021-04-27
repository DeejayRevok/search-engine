"""Change user source username with user id

Revision ID: 9cc430995408
Revises: 52136d106e7e
Create Date: 2021-01-06 12:28:31.171802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Column, DefaultClause

revision = '9cc430995408'
down_revision = '52136d106e7e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('user_source', 'username')
    op.add_column('user_source', Column('user_id', sa.Integer, DefaultClause(-1), nullable=False))


def downgrade():
    op.drop_column('user_source', 'user_id')
    op.add_column('user_source', Column('username', sa.String(255), DefaultClause(""), nullable=False))
