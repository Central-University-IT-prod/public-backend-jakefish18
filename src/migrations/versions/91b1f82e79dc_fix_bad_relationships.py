"""Fix bad relationships

Revision ID: 91b1f82e79dc
Revises: 39bebbc0d696
Create Date: 2024-03-25 19:57:07.035813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91b1f82e79dc'
down_revision: Union[str, None] = '39bebbc0d696'
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
