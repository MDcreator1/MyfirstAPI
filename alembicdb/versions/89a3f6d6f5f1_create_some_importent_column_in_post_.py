"""create some importent column in post table

Revision ID: 89a3f6d6f5f1
Revises: 6be4ea8a18e4
Create Date: 2026-03-21 11:45:06.005461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89a3f6d6f5f1'
down_revision: Union[str, Sequence[str], None] = '6be4ea8a18e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", 
                    sa.Column("content", sa.String(), nullable=False)
                )
    op.add_column("posts", 
                    sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.text('TRUE'))
                )
    op.add_column("posts", 
                    sa.Column("rating", sa.Integer(), server_default=sa.text("0"), nullable=True)
                )
    op.add_column("posts", 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
                )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
