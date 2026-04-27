"""Add is_favorite

Revision ID: 04feb5e9f466
Revises: a844cfdfc8e5
Create Date: 2026-04-27 20:12:05.188324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04feb5e9f466'
down_revision: Union[str, Sequence[str], None] = 'a844cfdfc8e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("notes", sa.Column('is_favorite', sa.Boolean(), nullable=True))

    op.execute("UPDATE notes SET is_favorite = false")

    op.alter_column('notes', 'is_favorite', existing_type= sa.Boolean(),nullable=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
