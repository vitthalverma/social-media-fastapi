"""add users table

Revision ID: fd4f22cea675
Revises: 3d7fa67f491d
Create Date: 2024-08-12 20:49:39.538524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd4f22cea675'
down_revision: Union[str, None] = '3d7fa67f491d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone= True), server_default = sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),     
    )
    pass


def downgrade():
    op.drop_table("users")
    pass