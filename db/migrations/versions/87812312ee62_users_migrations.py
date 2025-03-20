"""Users migrations

Revision ID: 87812312ee62
Revises: 797fea5002ac
Create Date: 2025-03-20 08:06:00.088832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87812312ee62'
down_revision: Union[str, None] = '797fea5002ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
