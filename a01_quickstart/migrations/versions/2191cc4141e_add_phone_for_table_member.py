"""add phone for table member

Revision ID: 2191cc4141e
Revises: 151de8c8a79
Create Date: 2015-10-23 17:16:02.013501

"""

# revision identifiers, used by Alembic.
revision = '2191cc4141e'
down_revision = '151de8c8a79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('phone', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member', 'phone')
    ### end Alembic commands ###
