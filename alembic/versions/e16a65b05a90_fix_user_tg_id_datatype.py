"""fix user_tg_id datatype

Revision ID: e16a65b05a90
Revises: 593930aea021
Create Date: 2024-10-26 09:53:39.294829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e16a65b05a90'
down_revision: Union[str, None] = '593930aea021'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
