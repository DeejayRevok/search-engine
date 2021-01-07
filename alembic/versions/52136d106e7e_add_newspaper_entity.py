"""Add newspaper entity

Revision ID: 52136d106e7e
Revises: 646283356301
Create Date: 2021-01-06 12:04:35.536819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52136d106e7e'
down_revision = '646283356301'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "newspaper",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False)
    )
    op.create_table(
        'newspaper_named_entity',
        sa.Column('newspaper_id', sa.Integer(), sa.ForeignKey('newspaper.id', ondelete='CASCADE')),
        sa.Column('named_entity_id', sa.Integer(), sa.ForeignKey('named_entity.id', ondelete='CASCADE'))
    )
    op.create_table(
        'newspaper_noun_chunk',
        sa.Column('newspaper_id', sa.Integer(), sa.ForeignKey('newspaper.id', ondelete='CASCADE')),
        sa.Column('noun_chunk_id', sa.Integer(), sa.ForeignKey('noun_chunk.id', ondelete='CASCADE'))
    )


def downgrade():
    op.drop_table('newspaper')
    op.drop_table('newspaper_named_entity')
    op.drop_table('newspaper_noun_chunk')
