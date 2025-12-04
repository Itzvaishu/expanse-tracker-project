"""add is_active to users

Revision ID: add_is_active
Revises: c1234567890a
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_active'
down_revision = 'c1234567890a'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_active column to users table
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, default=True))


def downgrade():
    # Remove is_active column from users table
    op.drop_column('users', 'is_active')
