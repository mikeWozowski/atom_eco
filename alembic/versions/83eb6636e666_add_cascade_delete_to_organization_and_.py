"""Add cascade delete to organization and storage fullness

Revision ID: 83eb6636e666
Revises: 57b58e99ad0c
Create Date: 2024-11-03 20:15:34.667165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83eb6636e666'
down_revision: Union[str, None] = '57b58e99ad0c'
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
