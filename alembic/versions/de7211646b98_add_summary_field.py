"""Add summary field

Revision ID: de7211646b98
Revises: 615836022320
Create Date: 2022-27-06 20:50:11.581230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Column

revision = 'de7211646b98'
down_revision = '615836022320'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('new', Column('summary', sa.Text, default=None, server_default=None, nullable=True))


def downgrade():
    op.drop_column('new', 'summary')
