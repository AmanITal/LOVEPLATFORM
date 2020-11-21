"""empty message

Revision ID: 5fe1a705580f
Revises: c0ff923eabe7
Create Date: 2019-04-29 11:56:29.370206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fe1a705580f'
down_revision = 'c0ff923eabe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('autograph', sa.String(length=255), server_default='这个人很懒', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'autograph')
    # ### end Alembic commands ###