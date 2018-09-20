"""empty message

Revision ID: d8a128ce003e
Revises: 6e6d8de9a79b
Create Date: 2018-09-19 23:35:08.839037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8a128ce003e'
down_revision = '6e6d8de9a79b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist_artwork', schema=None) as batch_op:
        batch_op.create_unique_constraint('UC_artist_id_artwork_id', ['artwork_id', 'artist_id'])
        batch_op.drop_constraint(u'UC_artwork_id_artist_id', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist_artwork', schema=None) as batch_op:
        batch_op.create_unique_constraint(u'UC_artwork_id_artist_id', ['artwork_id', 'artist_id'])
        batch_op.drop_constraint('UC_artist_id_artwork_id', type_='unique')

    # ### end Alembic commands ###
