"""add_role_id_to_users

Revision ID: b32b59a95fff
Revises: 305818650c75
Create Date: 2025-11-27 12:15:30.208040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b32b59a95fff'
down_revision: Union[str, None] = '305818650c75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add nullable role_id column and foreign key to roles(id)
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_role_id_roles', 'users', 'roles', ['role_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key then column
    op.drop_constraint('fk_users_role_id_roles', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
