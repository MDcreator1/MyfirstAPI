"""create posts table

Revision ID: 6be4ea8a18e4
Revises: 
Create Date: 2026-03-21 11:43:56.503619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6be4ea8a18e4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=False, primary_key = True), 
                    sa.Column("title", sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint("id")
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass