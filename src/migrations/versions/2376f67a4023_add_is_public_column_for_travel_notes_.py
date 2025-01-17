"""Add is_public column for travel_notes table

Revision ID: 2376f67a4023
Revises: b4360628681d
Create Date: 2024-03-25 19:24:42.598674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2376f67a4023'
down_revision: Union[str, None] = 'b4360628681d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('travel_notes', sa.Column('is_public', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('travel_notes', 'is_public')
    # ### end Alembic commands ###
