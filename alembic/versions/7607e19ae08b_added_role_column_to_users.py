"""Added role column to users

Revision ID: 7607e19ae08b
Revises: 8df451f04944
Create Date: 2025-11-26 14:24:07.336281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7607e19ae08b'
down_revision: Union[str, None] = '8df451f04944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add `role` column to users table; previous auto-generated content
    # looked like it would drop tables — replace with safe operation.
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=True, server_default='user'))


def downgrade() -> None:
    # Reverse: remove the `role` column
    op.drop_column('users', 'role')
