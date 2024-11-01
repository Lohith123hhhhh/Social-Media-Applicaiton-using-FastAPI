"""create posts table

Revision ID: 78157f9abc60
Revises: 
Create Date: 2024-10-26 16:11:27.020904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78157f9abc60'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),)
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
