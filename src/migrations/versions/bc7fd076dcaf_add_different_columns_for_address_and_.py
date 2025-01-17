"""Add different columns for address and city

Revision ID: bc7fd076dcaf
Revises: e69516c659f3
Create Date: 2024-03-20 13:42:13.758232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc7fd076dcaf'
down_revision: Union[str, None] = 'e69516c659f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('travel_cities', sa.Column('address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('travel_cities', 'address')
    # ### end Alembic commands ###
