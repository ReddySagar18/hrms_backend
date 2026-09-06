"""implement employee project relationship

Revision ID: 734f95a47022
Revises: f46b3f5019e6
Create Date: 2026-09-06 12:12:33.825621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '734f95a47022'
down_revision: Union[str, Sequence[str], None] = 'f46b3f5019e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
