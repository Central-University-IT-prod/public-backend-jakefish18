"""Fix bad realtionships

Revision ID: 3385c35d23b6
Revises: 028b4ed2d9b0
Create Date: 2024-03-21 16:37:35.663352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3385c35d23b6'
down_revision: Union[str, None] = '028b4ed2d9b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###