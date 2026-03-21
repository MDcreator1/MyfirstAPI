"""create users table

Revision ID: ac3395ac4a87
Revises: 89a3f6d6f5f1
Create Date: 2026-03-21 11:46:22.318418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac3395ac4a87'
down_revision: Union[str, Sequence[str], None] = '89a3f6d6f5f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable = False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
    )

    pass


def downgrade() -> None:
    op.drop_table("users")
    """Downgrade schema."""
    pass
