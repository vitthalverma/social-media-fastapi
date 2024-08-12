"""add last few columns to post table

Revision ID: 443e274dc497
Revises: 43164878cc9b
Create Date: 2024-08-12 21:08:54.877746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '443e274dc497'
down_revision: Union[str, None] = '43164878cc9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="True"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone= True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade():
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
