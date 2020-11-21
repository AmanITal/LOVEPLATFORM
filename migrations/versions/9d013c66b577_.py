"""empty message

Revision ID: 9d013c66b577
Revises: 60ba4d81a8a7
Create Date: 2019-05-01 20:49:26.400032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d013c66b577'
down_revision = '60ba4d81a8a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('characters_ibfk_1', 'characters', type_='foreignkey')
    op.create_foreign_key(None, 'characters', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('comments_ibfk_2', 'comments', type_='foreignkey')
    op.drop_constraint('comments_ibfk_1', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'life', ['life_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comments', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('friend_ibfk_1', 'friend', type_='foreignkey')
    op.create_foreign_key(None, 'friend', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('hobby_ibfk_1', 'hobby', type_='foreignkey')
    op.create_foreign_key(None, 'hobby', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('life_ibfk_1', 'life', type_='foreignkey')
    op.create_foreign_key(None, 'life', 'user', ['author_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'life', type_='foreignkey')
    op.create_foreign_key('life_ibfk_1', 'life', 'user', ['author_id'], ['id'])
    op.drop_constraint(None, 'hobby', type_='foreignkey')
    op.create_foreign_key('hobby_ibfk_1', 'hobby', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'friend', type_='foreignkey')
    op.create_foreign_key('friend_ibfk_1', 'friend', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_ibfk_1', 'comments', 'life', ['life_id'], ['id'])
    op.create_foreign_key('comments_ibfk_2', 'comments', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'characters', type_='foreignkey')
    op.create_foreign_key('characters_ibfk_1', 'characters', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
