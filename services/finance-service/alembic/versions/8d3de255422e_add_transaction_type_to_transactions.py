"""add transaction_type to transactions

Revision ID: 8d3de255422e
Revises: a53b938ee218
Create Date: 2026-03-08 00:45:00.020776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d3de255422e'
down_revision: Union[str, None] = 'a53b938ee218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("transaction_type", sa.String(), nullable=True),
        schema="finance",
    )


def downgrade() -> None:
    op.drop_column("transactions", "transaction_type", schema="finance")