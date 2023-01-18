"""
Initial migration

Revision ID: 1af4b780ddf8
Revises: 
Create Date: 2022-12-13 22:52:43.279341

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '1af4b780ddf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('named_entity_type',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('source',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('named_entity',
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('named_entity_type_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['named_entity_type_name'], ['named_entity_type.name'], ),
    sa.PrimaryKeyConstraint('value')
    )
    op.create_table('new',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('sentiment', sa.Numeric(), nullable=True),
    sa.Column('source_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['source_name'], ['source.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('newspaper',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_email', sa.String(length=320), nullable=False),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'user_email')
    )
    op.create_table('named_entity_new',
    sa.Column('named_entity_value', sa.String(), nullable=False),
    sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['named_entity_value'], ['named_entity.value'], ),
    sa.ForeignKeyConstraint(['new_id'], ['new.id'], ),
    sa.PrimaryKeyConstraint('named_entity_value', 'new_id')
    )
    op.create_table('named_entity_newspaper',
    sa.Column('named_entity_value', sa.String(), nullable=False),
    sa.Column('newspaper_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['named_entity_value'], ['named_entity.value'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['newspaper_id'], ['newspaper.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('named_entity_value', 'newspaper_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('named_entity_newspaper')
    op.drop_table('named_entity_new')
    op.drop_table('newspaper')
    op.drop_table('new')
    op.drop_table('named_entity')
    op.drop_table('users')
    op.drop_table('source')
    op.drop_table('named_entity_type')
    # ### end Alembic commands ###
