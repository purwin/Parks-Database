"""empty message

Revision ID: 6e6d8de9a79b
Revises: 94f305218ed5
Create Date: 2018-09-19 23:33:16.281237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e6d8de9a79b'
down_revision = '94f305218ed5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist_artwork', schema=None) as batch_op:
        batch_op.create_unique_constraint('UC_artwork_id_artist_id', ['artwork_id', 'artist_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist_artwork', schema=None) as batch_op:
        batch_op.drop_constraint('UC_artwork_id_artist_id', type_='unique')

    # ### end Alembic commands ###
