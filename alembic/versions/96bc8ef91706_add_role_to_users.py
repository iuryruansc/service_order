"""add role to users

Revision ID: 96bc8ef91706
Revises: 45e9d37ec4e8
Create Date: 2026-05-22 21:09:52.369082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96bc8ef91706'
down_revision: Union[str, Sequence[str], None] = '45e9d37ec4e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    userrole = sa.Enum("admin", "user", name="userrole")
    userrole.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "role",
                sa.Enum("admin", "user", name="userrole"),
                nullable=False,
                server_default="user",
            )
        )

def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("role")

    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
