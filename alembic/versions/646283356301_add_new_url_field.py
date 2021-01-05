"""Add new url field

Revision ID: 646283356301
Revises: 
Create Date: 2021-01-05 18:35:08.848100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Column, DefaultClause

revision = '646283356301'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('new', Column('url', sa.String(2083), DefaultClause(""), nullable=False))


def downgrade():
    op.drop_column('new', 'url')
