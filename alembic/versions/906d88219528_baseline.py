"""baseline

Revision ID: 906d88219528
Revises: 
Create Date: 2026-08-30 09:40:07.042902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '906d88219528'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline existing database schema."""
    pass
    


def downgrade() -> None:
    """Baseline has nothing to downgrade."""
    pass
