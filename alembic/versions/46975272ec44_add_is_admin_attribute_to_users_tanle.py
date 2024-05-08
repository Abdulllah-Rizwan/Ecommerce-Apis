"""add is_admin attribute to users tanle

Revision ID: 46975272ec44
Revises: ab54fa8c51cb
Create Date: 2024-05-07 08:31:23.294495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46975272ec44'
down_revision: Union[str, None] = 'ab54fa8c51cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
