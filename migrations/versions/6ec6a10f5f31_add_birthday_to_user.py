"""Add birthday to user

Revision ID: 6ec6a10f5f31
Revises: 0425279bc2cd
Create Date: 2022-05-19 16:16:14.128553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ec6a10f5f31'
down_revision = '0425279bc2cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birthday', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'birthday')
    # ### end Alembic commands ###
