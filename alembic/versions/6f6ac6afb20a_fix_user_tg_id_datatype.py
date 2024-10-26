"""fix user_tg_id datatype

Revision ID: 6f6ac6afb20a
Revises: e16a65b05a90
Create Date: 2024-10-26 09:55:05.409131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f6ac6afb20a'
down_revision: Union[str, None] = 'e16a65b05a90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
