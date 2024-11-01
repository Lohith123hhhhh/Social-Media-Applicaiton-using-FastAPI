"""add content column

Revision ID: b20b7e108936
Revises: 78157f9abc60
Create Date: 2024-10-26 18:31:27.335912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b20b7e108936'
down_revision: Union[str, None] = '78157f9abc60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(length=255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
