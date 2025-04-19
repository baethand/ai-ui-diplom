"""Init

Revision ID: b67285866b6d
Revises: c22662fd571c
Create Date: 2025-04-19 19:52:28.904085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b67285866b6d'
down_revision: Union[str, None] = 'c22662fd571c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
