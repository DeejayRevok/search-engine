"""add user new entity

Revision ID: ad553480c481
Revises: 9cc430995408
Create Date: 2021-03-06 12:16:32.372922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad553480c481'
down_revision = '9cc430995408'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_new",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE'))
    )


def downgrade():
    op.drop_table('user_new')
