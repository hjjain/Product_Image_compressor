"""Initial migration

Revision ID: 0fa15a5fd3dd
Revises: 
Create Date: 2025-02-25 18:04:24.781677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fa15a5fd3dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('request_id', sa.UUID(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('input_url', sa.String(), nullable=True),
    sa.Column('output_url', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('requests')
    # ### end Alembic commands ###
