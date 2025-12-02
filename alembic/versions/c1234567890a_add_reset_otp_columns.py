"""add reset otp columns

Revision ID: c1234567890a
Revises: b32b59a95fff
Create Date: 2025-11-27 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1234567890a'
down_revision: Union[str, None] = 'b32b59a95fff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add reset_otp and otp_expiry columns to users table
    op.add_column('users', sa.Column('reset_otp', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('otp_expiry', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Drop the columns
    op.drop_column('users', 'otp_expiry')
    op.drop_column('users', 'reset_otp')
