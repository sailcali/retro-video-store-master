"""empty message

Revision ID: 36a903bae957
Revises: ee190e18f2f7
Create Date: 2021-11-08 21:36:01.438772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36a903bae957'
down_revision = 'ee190e18f2f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('total_inventory', sa.Integer(), nullable=True))
    op.drop_column('video', 'inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('video', 'total_inventory')
    # ### end Alembic commands ###
