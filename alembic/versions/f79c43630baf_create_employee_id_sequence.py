"""Create employee ID sequence

Revision ID: f79c43630baf
Revises: 928613c3a8b4
Create Date: 2026-09-27 17:18:53.020914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f79c43630baf'
down_revision: Union[str, Sequence[str], None] = '928613c3a8b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS employee_id_seq
        MINVALUE 1
        START WITH 1
        INCREMENT BY 1
    """)

    op.execute("""
        DO $$
        DECLARE
            max_employee_number INTEGER;
        BEGIN
            SELECT MAX(
                CAST(SUBSTRING(employee_id FROM 4) AS INTEGER)
            )
            INTO max_employee_number
            FROM employees
            WHERE employee_id ~ '^EMP[0-9]+$';

            IF max_employee_number IS NULL THEN
                PERFORM setval(
                    'employee_id_seq',
                    1,
                    false
                );
            ELSE
                PERFORM setval(
                    'employee_id_seq',
                    max_employee_number,
                    true
                );
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.execute("""
        DROP SEQUENCE IF EXISTS employee_id_seq
    """)
