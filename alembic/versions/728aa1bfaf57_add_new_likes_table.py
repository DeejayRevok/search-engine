"""Add new likes table

Revision ID: 728aa1bfaf57
Revises: cd7211646b97
Create Date: 2021-03-07 22:19:14.323858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '728aa1bfaf57'
down_revision = 'cd7211646b97'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "new_like",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE'))
    )


def downgrade():
    op.drop_table('new_like')
