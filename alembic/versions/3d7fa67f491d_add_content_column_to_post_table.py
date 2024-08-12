"""add content column to post table

Revision ID: 3d7fa67f491d
Revises: 6e780ce47b9f
Create Date: 2024-08-12 20:42:14.958554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d7fa67f491d'
down_revision: Union[str, None] = '6e780ce47b9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable= False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
