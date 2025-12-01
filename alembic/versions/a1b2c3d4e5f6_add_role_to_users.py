"""Add role column to users

Revision ID: a1b2c3d4e5f6
Revises: 7607e19ae08b
Create Date: 2025-11-26 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '7607e19ae08b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add `role` column to users with default 'user'
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=True, server_default='user'))


def downgrade() -> None:
    # Remove the `role` column
    op.drop_column('users', 'role')
