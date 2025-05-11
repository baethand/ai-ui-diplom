"""Update

Revision ID: 645cc069718f
Revises: 315da8249bf7
Create Date: 2025-05-03 15:20:03.447704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '645cc069718f'
down_revision: Union[str, None] = '315da8249bf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
