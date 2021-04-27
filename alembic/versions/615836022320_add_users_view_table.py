"""Add users view table

Revision ID: 615836022320
Revises: 728aa1bfaf57
Create Date: 2021-03-08 17:03:17.666959

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import DefaultClause

revision = '615836022320'
down_revision = '728aa1bfaf57'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('username', sa.String(255))
    )
    op.drop_table('newspaper_follow')
    op.create_table(
        'newspaper_follow',
        sa.Column('newspaper_id', sa.Integer(), sa.ForeignKey('newspaper.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'))
    )

    op.drop_table('user_new')
    op.create_table(
        'user_new',
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'))
    )

    op.drop_table('new_like')
    op.create_table(
        'new_like',
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'))
    )

    op.drop_table('user_source')
    op.create_table(
        'source_follow',
        sa.Column('source_id', sa.Integer(), sa.ForeignKey('source.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'))
    )

    op.drop_column('newspaper', 'user_id')
    op.add_column('newspaper',
                  sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False))


def downgrade():
    op.drop_table('user')

    op.drop_table('newspaper_follow')
    op.create_table(
        "newspaper_follow",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('newspaper_id', sa.Integer(), sa.ForeignKey('newspaper.id', ondelete='CASCADE'))
    )

    op.drop_table('user_new')
    op.create_table(
        "user_new",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE'))
    )

    op.drop_table('new_like')
    op.create_table(
        "new_like",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('new_id', sa.Integer(), sa.ForeignKey('new.id', ondelete='CASCADE'))
    )

    op.drop_table('source_follow')
    op.create_table(
        'user_source',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('source_id', sa.Integer(), sa.ForeignKey('source.id', ondelete='CASCADE'))
    )

    op.drop_column('newspaper', 'user_id')
    op.add_column('newspaper', sa.Column('user_id', sa.Integer, DefaultClause(-1), nullable=False))
