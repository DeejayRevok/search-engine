"""Add followed newspapers entity

Revision ID: cd7211646b97
Revises: ad553480c481
Create Date: 2021-03-07 11:50:11.581230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd7211646b97'
down_revision = 'ad553480c481'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "newspaper_follow",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('newspaper_id', sa.Integer(), sa.ForeignKey('newspaper.id', ondelete='CASCADE'))
    )


def downgrade():
    op.drop_table('newspaper_follow')
