"""create foreign key

Revision ID: ab95094825b0
Revises: ac3395ac4a87
Create Date: 2026-03-21 11:47:36.408489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab95094825b0'
down_revision: Union[str, Sequence[str], None] = 'ac3395ac4a87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts", type = "foreignkey" )
    op.drop_column("posts", "owner_id")
    pass

