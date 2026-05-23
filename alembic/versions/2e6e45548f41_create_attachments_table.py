"""create attachments table

Revision ID: 2e6e45548f41
Revises: 96bc8ef91706
Create Date: 2026-05-23 10:58:49.382447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e6e45548f41'
down_revision: Union[str, Sequence[str], None] = '96bc8ef91706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('attachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_order_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('file_path', sa.String(length=150), nullable=False),
    sa.Column('uploaded_by_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['service_order_id'], ['service_orders.id'], ),
    sa.ForeignKeyConstraint(['uploaded_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attachments_id'), 'attachments', ['id'], unique=False)

    with op.batch_alter_table("service_orders") as batch_op:
        batch_op.alter_column('responsible_user_id', existing_type=sa.INTEGER(), nullable=False)

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column('role', existing_type=sa.VARCHAR(length=5), type_=sa.String(length=50), existing_nullable=False)

def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column('role', existing_type=sa.String(length=50), type_=sa.VARCHAR(length=5), existing_nullable=False)

    with op.batch_alter_table("service_orders") as batch_op:
        batch_op.alter_column('responsible_user_id', existing_type=sa.INTEGER(), nullable=True)

    op.drop_index(op.f('ix_attachments_id'), table_name='attachments')
    op.drop_table('attachments')
