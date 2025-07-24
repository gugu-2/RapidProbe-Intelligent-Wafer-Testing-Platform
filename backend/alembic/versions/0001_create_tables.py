"""
Revision ID: 0001
Revises: 
Create Date: 2025-07-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'wafers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('batch_id', sa.String, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )
    op.create_table(
        'test_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('wafer_id', sa.Integer, sa.ForeignKey('wafers.id')),
        sa.Column('die_x', sa.Integer),
        sa.Column('die_y', sa.Integer),
        sa.Column('test_name', sa.String),
        sa.Column('result_value', sa.Float),
        sa.Column('timestamp', sa.DateTime, nullable=False)
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('hashed_pw', sa.String),
        sa.Column('role', sa.String)
    )

def downgrade():
    op.drop_table('users')
    op.drop_table('test_results')
    op.drop_table('wafers')
