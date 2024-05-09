"""includes price in stock

Revision ID: 8b729b8205b3
Revises: dffa8a62e108
Create Date: 2024-05-07 15:33:41.302044

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b729b8205b3"
down_revision: Union[str, None] = "dffa8a62e108"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("stocks", sa.Column("price", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("stocks", "price")
    # ### end Alembic commands ###